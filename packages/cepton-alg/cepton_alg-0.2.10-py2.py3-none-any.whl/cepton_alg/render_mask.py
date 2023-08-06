import numpy
import PIL.Image
import PIL.ImageDraw
from pykdtree.kdtree import KDTree

import cepton_alg.c
import cepton_alg.core
from cepton_alg.common import *
from cepton_alg.common.render_vispy import *

_all_builder = AllBuilder(__name__)


def _from_image(image):
    return numpy.asarray(image)


def _to_image(a, mode="1"):
    # HACK: Image.fromarray broken
    assert(mode == "1")
    a_bytes = numpy.packbits(a, axis=1)
    a_bytes = cepton_alg.c.get_c_ndarray(a_bytes)
    options = {
        "size": a.shape[::-1],
        "data": a_bytes,
        "mode": mode,
    }
    return PIL.Image.frombytes(**options)


class GridImageEditor(InteractiveWidget):
    def __init__(self, **kwargs):
        self.brush_size = 1
        self.transform = vispy.visuals.transforms.NullTransform()

        self.visual = CompoundVisual([])

        self._brush_visual = CirclesVisual()
        self.visual.add_subvisual(self._brush_visual)

        super().__init__(**kwargs)

        self.clear()

        def on_timer(*args):
            self._update_values()
        options = {
            "connect": on_timer,
            "interval": 0.2,
            "start": True,
        }
        self._timer = vispy.app.Timer(**options)

    def _from_image(self, image):
        return _from_image(self._image).transpose()

    def _to_image(self, a, **kwargs):
        return _to_image(a.transpose(), **kwargs)

    @property
    def values(self):
        return self._from_image(self._image)

    def set_data(self, grid, values=None, mode="1"):
        assert(grid.n_dims == 2)

        self.grid = grid
        if values is None:
            self._image = PIL.Image.new(mode, tuple(self.grid.shape))
        else:
            values = values.reshape(self.grid.shape)
            self._image = self._to_image(values, mode=mode)
        self._draw = PIL.ImageDraw.Draw(self._image)

    def fill_values(self, fill=0):
        self._draw.rectangle([(0, 0), self._image.size], fill=fill)

    def clear(self):
        self._previous_brush_position = None
        self._brush_position = None

        self._brush_visual.clear()

    def _update_values(self):
        pass

    @property
    def _image_brush_size(self):
        return numpy.around(self.brush_size / self.grid.spacing[0]).astype(int)

    def _get_image_idx(self, position):
        position = self.transform.imap(position)
        return self.grid.get_indices(position[:2])[0, :]

    def _draw_circle(self, center, radius, **kwargs):
        self._draw.ellipse(
            [tuple(center - radius + 1), tuple(center + radius - 1)], **kwargs)

    def _draw_thick_line(self, x1, x2, width, **kwargs):
        self._draw.line([tuple(x1), tuple(x2)], width=width, **kwargs)
        self._draw_circle(x1, width, **kwargs)
        self._draw_circle(x2, width, **kwargs)

    def on_mouse_press(self, event, view):
        if not self.enabled:
            return False

        if set(event.modifiers) == {vispy.util.keys.CONTROL}:
            if event.button in [1, 2]:
                position = get_mouse_event_position(event, view)
                if self._brush_position is not None:
                    if event.button == 1:
                        brush_fill = 1
                    else:
                        brush_fill = 0
                    image_idx = self._get_image_idx(self._brush_position)
                    self._draw_circle(
                        image_idx, self._image_brush_size, fill=brush_fill)
                return True
        return False

    def on_mouse_move(self, event, view):
        if not self.enabled:
            return False

        self._previous_brush_position = self._brush_position

        # Update brush
        line = get_mouse_event_line(event, view)
        plane = cepton_alg.common.geometry.Plane()
        plane.normal[:, :] = [0, 0, 1]
        self._brush_position = \
            cepton_alg.common.geometry.plane_line_intersection(
                plane, line)[0, :]
        if numpy.any(numpy.isnan(self._brush_position)):
            self._brush_position = None
        self.update()

        if set(event.modifiers) == {vispy.util.keys.CONTROL}:
            if event.button in [1, 2]:
                if (self._previous_brush_position is not None) and (self._brush_position is not None):
                    if event.button == 1:
                        brush_fill = 1
                    else:
                        brush_fill = 0
                    previous_image_idx = self._get_image_idx(
                        self._previous_brush_position)
                    image_idx = self._get_image_idx(self._brush_position)
                    self._draw_thick_line(previous_image_idx, image_idx,
                                          self._image_brush_size, fill=brush_fill)
                return True

        return False

    def on_mouse_wheel(self, event):
        if set(event.modifiers) == {vispy.util.keys.CONTROL}:
            self.brush_size += event.delta[1]
            return True
        return False

    def _update_brush(self):
        if self._brush_position is None:
            self._brush_visual.clear()
            return

        options = {
            "n_theta": 100,
        }
        self._brush_visual.set_data(
            self._brush_position, self.brush_size, **options)

    def update(self):
        if not self.enabled:
            return
        self._update_brush()


class GridImageMaskEditor(GridImageEditor):
    def __init__(self, mask_id, **kwargs):
        self.mask_id = mask_id
        self.mask_enabled = False
        self.mask_relative = cepton_alg.core.is_grid_mask_relative(mask_id)

        # Not part of compound visual because requires transform
        self.mask_visual = BinaryGridImageVisual()

        super().__init__(**kwargs)

        grid = cepton_alg.common.geometry.Grid(2)
        grid.lb[:] = -300
        grid.spacing[:] = 1
        grid.set_shape_by_ub(-1 * grid.lb)
        super().set_data(grid)
        self.reset_mask()

    def _set_enabled(self, value):
        super()._set_enabled(value)
        self.mask_visual.visible = value

    @property
    def mask_indices(self):
        values = numpy.asarray(self._image, dtype=bool).transpose()
        return numpy.flatnonzero(values)

    @property
    def mask(self):
        mask = cepton_alg.core.GridMask()
        mask.enabled = self.mask_enabled
        mask.relative = self.mask_relative
        mask.inverted = False
        mask.grid = self.grid
        mask.indices = self.mask_indices
        return mask

    def clear(self):
        super().clear()
        self.mask_visual.clear()

    def _update_values(self):
        super()._update_values()

        if not self.enabled:
            return

        options = {
            "transform": self.transform,
        }
        self.mask_visual.set_data(
            self.grid, self.values, **options)

    def set_data(self, mask):
        # assert(mask.relative == self.mask_relative)
        assert(mask.inverted == False)

        values = numpy.zeros([len(mask.grid)], dtype=bool)
        values[mask.indices] = True
        values = values.reshape(mask.grid.shape)

        if len(mask.grid) == 0:
            self.fill_values()
        else:
            # Interpolate to current grid
            if mask.grid != self.grid:
                image = self._to_image(values, mode="1")
                scale = (self.grid.ptp / mask.grid.ptp)
                translation = (self.grid.lb - mask.grid.lb * scale)
                data = [
                    scale[0], 0, translation[0],
                    0, scale[1], translation[1],
                ]
                options = {
                    "data": data,
                    "fill": 0,
                    "resample": PIL.Image.NEAREST,
                }
                image = image.transform(
                    self.grid.size, PIL.Image.AFFINE, **options)
                values = self._from_image(image)
            super().set_data(self.grid, values)
        self.mask_enabled = mask.enabled

    def reset_mask(self):
        self.fill_values()
        self.mask_enabled = False

    def reload_mask(self):
        mask = cepton_alg.core.get_grid_mask(self.mask_id)
        if mask is None:
            self.reset_mask()
        else:
            self.set_data(mask)

    def save_mask(self):
        cepton_alg.core.set_grid_mask(self.mask_id, self.mask)


class GridMaskEditor:
    """Remove 3d regions."""

    def __init__(self, mask_id, **kwargs):
        self._enabled = False
        self.mask_id = mask_id
        self.mask_enabled = False
        self.mask_relative = cepton_alg.core.is_grid_mask_relative(mask_id)

        # Not part of compound visual because requires transform
        self.mask_visual = MarkersVisual()

        super().__init__(**kwargs)

        grid = cepton_alg.common.geometry.Grid(3)
        grid.lb[:] = -100
        grid.spacing[:] = 0.25
        grid.set_shape_by_ub(-1 * grid.lb)
        assert(grid.check())
        self.grid = grid
        self._update_tree()
        self.reset_mask()

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if value == self._enabled:
            return
        if self._enabled and (not value):
            self.clear()
        self._enabled = value
        self.mask_visual.visible = value

    def clear(self):
        pass

    @property
    def mask(self):
        mask = cepton_alg.core.GridMask()
        mask.enabled = self.mask_enabled
        mask.relative = self.mask_relative
        mask.inverted = True
        mask.grid = self.grid
        mask.indices = self.mask_indices
        return mask

    def _update_tree(self):
        grid = cepton_alg.common.geometry.Grid(3)
        grid.lb[:] = -5
        grid.spacing[:] = self.grid.spacing
        grid.set_shape_by_ub(-1 * grid.lb)
        self.tree_grid = grid
        x_list = []
        for i in range(3):
            x = numpy.arange(self.tree_grid.shape[i]) * self.tree_grid.spacing[i] + \
                self.tree_grid.lb[i]
            x_list.append(x)
        grid_positions = numpy.meshgrid(*x_list, indexing="ij")
        grid_positions = numpy.stack(
            [x.flat for x in grid_positions], axis=-1)
        self.tree = KDTree(grid_positions)

    def set_data(self, mask):
        assert(mask.grid.n_dims == 3)
        # assert(mask.relative == self.mask_relative)
        assert(mask.inverted == True)

        indices = mask.indices

        # Interpolate to grid
        if (mask.grid != self.grid):
            positions = mask.grid.get_flat_positions(indices)
            indices = self.grid.get_flat_indices(positions)

        self.mask_indices = indices
        self.mask_enabled = mask.enabled
        self._update_mask()

    def reset_mask(self):
        self.mask_indices = numpy.array([], dtype=int)
        self.mask_enabled = False
        self._update_mask()

    def reload_mask(self):
        mask = cepton_alg.core.get_grid_mask(self.mask_id)
        if mask is None:
            self.reset_mask()
        else:
            self.set_data(mask)

    def save_mask(self):
        cepton_alg.core.set_grid_mask(self.mask_id, self.mask)

    def add_balls(self, positions, radius=None):
        if self.tree is None:
            return
        positions = numpy.reshape(positions, [-1, 3])
        n = positions.shape[0]

        # Shift to tree grid
        grid_indices = self.grid.get_indices(positions)
        grid_positions = self.grid.get_positions(grid_indices)
        positions -= grid_positions

        # Find neighbors
        if radius is None:
            radius = self.grid.spacing[0]
        radius = max(radius, self.grid.spacing[0])
        k = int(numpy.prod(numpy.ceil(2 * radius / self.grid.spacing)))
        options = {
            "k": k,
            "distance_upper_bound": radius,
        }
        distances, indices = self.tree.query(positions, **options)
        distances = distances.flatten()
        indices = indices.flatten()
        offsets = numpy.repeat(numpy.arange(n)[:, numpy.newaxis],
                               k, axis=1).flatten()

        is_valid = numpy.isfinite(distances)
        indices = indices[is_valid]
        offsets = offsets[is_valid]

        # Shift back to grid
        positions = self.tree_grid.get_flat_positions(indices)
        positions += grid_positions[offsets, :]
        indices = self.grid.get_flat_indices(positions)

        indices = indices[indices >= 0]
        self.mask_indices = numpy.union1d(self.mask_indices, indices)
        self._update_mask()

    def _update_mask(self):
        if not self.enabled:
            return

        positions = self.grid.get_flat_positions(self.mask_indices)
        options = {
            "pos": positions,
            "size": self.grid.spacing[0],
            "scaling": True,
            "edge_width": 0,
            "face_color": [0.5, 0.5, 0.5, 0.5],
        }
        self.mask_visual.set_data(**options)


__all__ = _all_builder.get()
