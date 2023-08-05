import enum
import os.path
import pkgutil
import pprint
import time

import imageio
import numpy
import scipy.interpolate
import seaborn
import stl
import transforms3d.euler

import cepton_alg.common.geometry
import cepton_alg.common.render
import cepton_alg.common.time
import cepton_util.common
from cepton_alg.common import *

_all_builder = AllBuilder(__name__)


from cepton_alg.common.render import *  # noqa isort:skip
import vispy.app  # noqa isort:skip
import vispy.io  # noqa isort:skip
import vispy.scene  # noqa isort:skip
import vispy.scene.cameras.turntable  # noqa isort:skip
import vispy.util.keys  # noqa isort:skip

vispy.use(app="PyQt5")


def get_mouse_event_position(event, view):
    position = view.scene.transform.imap(
        [event.pos[0], event.pos[1], 0, 1])
    return numpy.array(position[:3])


def get_mouse_event_direction(event, view):
    transform = view.scene.transform
    direction = transform.imap([0, 0, 1, 1]) - transform.imap([0, 0, 0, 1])
    return vector_normalize(direction[:3])


def get_mouse_event_line(event, view):
    line = cepton_alg.common.geometry.Line()
    line.position[:, :] = get_mouse_event_position(event, view)
    line.direction[:, :] = get_mouse_event_direction(event, view)
    return line


def wrap_visual(cls):
    class Visual:
        def __init__(self, **kwargs):
            self.visual = vispy.scene.visuals.Compound([])
            self._visual = cls(**kwargs)
            self.visual.add_subvisual(self._visual)

        def clear(self):
            self._visual.visible = False

        def set_data(self, *args, **kwargs):
            self._visual.visible = True
            self._visual.set_data(*args, **kwargs)
    return Visual


LineVisual = wrap_visual(vispy.scene.visuals.Line)
MeshVisual = wrap_visual(vispy.scene.visuals.Mesh)
TextVisual = wrap_visual(vispy.scene.visuals.Text)


class MarkersVisual(wrap_visual(vispy.scene.visuals.Markers)):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._visual.antialias = 0


class InteractiveWidget:
    def __init__(self):
        self._enabled = False

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self.clear()
        self._enabled = value

    def on_mouse_press(self, event, view):
        return False

    def on_mouse_release(self, event, view):
        return False

    def on_mouse_move(self, event, view):
        return False

    def on_key_press(self, event):
        return False

    def clear(self):
        pass


class DistanceRuler(InteractiveWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.visual = vispy.scene.visuals.Compound([])
        self._init_text()
        self._init_lines()

        self.clear()

    def clear(self):
        self._start = None
        self._end = None

        self._text_visual.visible = False
        self._lines_visual.visible = False

    def _init_text(self):
        options = {
            "bold": True,
            "color": "red",
            "font_size": 18,
        }
        self._text_visual = vispy.scene.visuals.Text(**options)
        self.visual.add_subvisual(self._text_visual)

    def _init_lines(self):
        options = {
            "antialias": True,
            "connect": "segments",
        }
        self._lines_visual = vispy.scene.visuals.Line(**options)
        self.visual.add_subvisual(self._lines_visual)

    def on_mouse_press(self, event, view):
        if not self.enabled:
            return False
        if set(event.modifiers) == {vispy.util.keys.CONTROL}:
            position = get_mouse_event_position(event, view)
            if event.button == 1:
                # Set start
                self._start = position
                self._end = position
                self.update()
                return True
        return False

    def on_mouse_move(self, event, view):
        if not self.enabled:
            return False
        if set(event.modifiers) == {vispy.util.keys.CONTROL}:
            position = get_mouse_event_position(event, view)
            if event.button == 1:
                # Set end
                self._end = position
                self.update()
                return True
        return True

    def _update_text(self):
        distance = vector_norm(self._end - self._start)

        self._text_visual.pos = self._start
        self._text_visual.text = "{:.2f}m".format(distance)
        self._text_visual.visible = True

    def _update_lines(self):
        vertices = [self._start, self._end]
        options = {
            "color": "red",
            "pos": numpy.vstack(vertices),
        }
        self._lines_visual.set_data(**options)
        self._lines_visual.visible = True

    def update(self):
        if not self.enabled:
            return
        if self._start is None:
            return
        self._update_text()
        self._update_lines()


class AngleRuler(InteractiveWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.visual = vispy.scene.visuals.Compound([])
        self._init_text()
        self._init_lines()

        self.clear()

    def clear(self):
        self.center = numpy.zeros([3])
        self._start = None
        self._end = None

        self._text_visual.visible = False
        self._lines_visual.visible = False

    def on_mouse_press(self, event, view):
        if not self.enabled:
            return False
        if set(event.modifiers) == {vispy.util.keys.CONTROL}:
            position = get_mouse_event_position(event, view)
            if event.button == 1:
                # Set start
                self._start = vector_normalize(position - self.center)
                if vector_norm(self._start) == 0:
                    self._start = None
                self._end = self._start
                self.update()
                return True
            elif event.button == 2:
                # Set center
                self.center = position
                self._start = None
                self._end = None
                self.update()
                return True
        return False

    def on_mouse_move(self, event, view):
        if not self.enabled:
            return False
        if set(event.modifiers) == {vispy.util.keys.CONTROL}:
            position = get_mouse_event_position(event, view)
            if event.button == 1:
                self._end = vector_normalize(position - self.center)
                if vector_norm(self._end) == 0:
                    self._end = self._start
                self.update()
                return True
        return True

    def _init_text(self):
        options = {
            "bold": True,
            "color": "red",
            "font_size": 18,
        }
        self._text_visual = vispy.scene.visuals.Text(**options)
        self.visual.add_subvisual(self._text_visual)

    def _init_lines(self):
        options = {
            "antialias": True,
            "connect": "segments",
        }
        self._lines_visual = vispy.scene.visuals.Line(**options)
        self.visual.add_subvisual(self._lines_visual)

    def _update_text(self):
        d = numpy.clip(vector_dot(self._start, self._end), 0, 1)
        angle = numpy.arccos(d)

        self._text_visual.pos = self.center
        self._text_visual.text = "{:.2f}°".format(numpy.degrees(angle))
        self._text_visual.visible = True

    def _update_lines(self):
        vertices = [
            self.center,
            self.center + 1000 * self._start,
            self.center,
            self.center + 1000 * self._end,
        ]
        options = {
            "color": "red",
            "pos": numpy.vstack(vertices),
        }
        self._lines_visual.set_data(**options)
        self._lines_visual.visible = True

    def update(self):
        if not self.enabled:
            return
        if self._start is None:
            return
        self._update_text()
        self._update_lines()


class BallsVisual(MarkersVisual):
    def set_data(self, balls, **kwargs):
        options = {
            "pos": balls.centerd,
            "size": balls.radius,
        }
        options.update(kwargs)
        super().set_data(**options)


class EdgesVisual(LineVisual):
    """Draw 3d lines given vertices and edges."""

    def set_data(self, vertices, edges, colors=None, **kwargs):
        if len(vertices) == 0:
            self.clear()
            return
        self._visual.visible = True

        if colors is not None:
            colors = numpy.repeat(colors[:, numpy.newaxis, :], 2, axis=1)
            colors = colors.reshape([-1, 4])

        options = {
            "color": colors,
            "connect": "segments",
            "pos": vertices[edges, :].reshape([-1, 3]),
        }
        options.update(kwargs)
        self._visual.set_data(**options)


def _create_wire_unit_box(n_dims):
    if (n_dims == 0):
        vertices = numpy.zeros([1, 1])
        edges = numpy.zeros([0, 2], dtype=int)
        return vertices, edges

    dim_spacing = 2**(n_dims - 1)

    vertices_tmp, edges_tmp = _create_wire_unit_box(n_dims - 1)
    n_vertices_tmp = vertices_tmp.shape[0]
    n_edges_tmp = edges_tmp.shape[0]

    vertices = numpy.zeros([2 * n_vertices_tmp, n_dims])
    vertices[:n_vertices_tmp, :-1] = vertices_tmp
    vertices[n_vertices_tmp:, :-1] = vertices_tmp
    vertices[n_vertices_tmp:, -1] = 1.0

    edges = numpy.zeros([n_vertices_tmp, 2])
    edges[:, 0] = numpy.arange(0, n_vertices_tmp)
    edges[:, 1] = edges[:, 0] + n_vertices_tmp
    edges = numpy.vstack(
        [edges_tmp, edges_tmp + n_vertices_tmp, edges]).astype(int)

    return vertices, edges


def create_wire_boxes(boxes):
    n = len(boxes)

    vertices_tmp, edges_tmp = _create_wire_unit_box(3)

    pad = 0.25
    vertices = numpy.repeat(vertices_tmp[numpy.newaxis, :, :], n, axis=0)
    vertices = (vertices - 0.5) * \
        (boxes.dimensions[:, numpy.newaxis, :] + 2 * pad)
    vertices = vertices.reshape([-1, 3])
    transforms = boxes.transform[numpy.repeat(
        numpy.arange(n), vertices_tmp.shape[0])]
    vertices = transforms.apply(vertices)

    edges = numpy.repeat(edges_tmp[numpy.newaxis, :, :], n, axis=0)
    edges = edges + vertices_tmp.shape[0] * \
        numpy.arange(n)[:, numpy.newaxis, numpy.newaxis]
    edges = edges.astype(int).reshape([-1, 2])

    return vertices, edges


class BoxesVisual(EdgesVisual):
    def set_data(self, boxes, colors=None, **kwargs):
        vertices, edges = create_wire_boxes(boxes)

        if colors is not None:
            unit_vertices, unit_edges = _create_wire_unit_box(3)
            colors = numpy.repeat(
                colors[:, numpy.newaxis, :], unit_edges.shape[0], axis=1)
            colors = colors.reshape([-1, 4])

        options = {
            "colors": colors,
        }
        options.update(kwargs)
        super().set_data(vertices, edges, **options)


class VectorsVisual(LineVisual):
    """Draw 3d vectors given positions and directions."""

    def set_data(self, positions, vectors, colors=numpy.ones([4]), **kwargs):
        if len(positions) == 0:
            self.clear()
            return
        self._visual.visible = True

        # Broadcast colors
        colors = numpy.broadcast_to(colors, [positions.shape[0], 4])

        # Create vertices
        vertices = [
            positions,
            positions + vectors,
        ]
        colors = numpy.broadcast_to(colors[:, numpy.newaxis, :], [
                                    positions.shape[0], 2, 4])

        options = {
            "color": colors,
            "connect": "segments",
            "pos": numpy.stack(vertices, axis=1).reshape([-1, 3]),
        }
        options.update(kwargs)
        self._visual.set_data(positions, **options)


class ThickLineVisual:
    """Draw thick 3d lines."""

    def __init__(self):
        self.visual = vispy.scene.visuals.Compound([])
        self._visual = None

    def clear(self):
        self._visual.visible = False

    def set_data(self, positions, **kwargs):
        if self._visual is not None:
            self.visual.remove_subvisual(self._visual)

        options = {
            "points": positions,
            "radius": 0.1,
            "shading": "flat",
            "tube_points": 4,
        }
        options.update(kwargs)
        self._visual = vispy.scene.visuals.Tube(**options)
        self._visual.ambient_light_color = "white"
        self._visual.shininess = 0
        self.visual.add_subvisual(self._visual)


class LineVisual:
    def __init__(self):
        self.visual = vispy.scene.visuals.Compound([])
        self._visual = vispy.scene.visuals.Line()
        self.visual.add_subvisual(self._visual)

    def clear(self):
        self._visual.visible = False

    def set_data(self, positions, **kwargs):
        if len(positions) == 0:
            self._visual.visible = False
            return
        self._visual.visible = True

        options = {
            "pos": positions,
        }
        options.update(**kwargs)
        self._visual.set_data(**options)


class CirclesVisual(LineVisual):
    def set_data(self, centers, radii, n_theta=10, colors=None, **kwargs):
        centers = numpy.reshape(centers, [-1, 1, 3])
        radii = numpy.reshape(radii, [-1, 1])
        if colors is not None:
            colors = numpy.reshape(colors, [-1, 1, 4])
        n_radii = radii.shape[0]

        theta = numpy.linspace(0, 2 * numpy.pi, n_theta)[numpy.newaxis, :]

        positions = numpy.zeros([n_radii, n_theta, 3])
        positions[:, :, 0] = radii * numpy.cos(theta)
        positions[:, :, 1] = radii * numpy.sin(theta)
        positions[:, :, :] += centers

        # Cut lines
        positions = numpy.insert(positions, 0, numpy.nan, axis=1)
        positions = positions.reshape([-1, 3])
        if colors is not None:
            colors = numpy.broadcast_to(colors, [n_radii, n_theta, 4])
            colors = numpy.insert(colors, 0, numpy.nan, axis=1)
            colors = colors.reshape([-1, 4])

        options = {}
        if colors is not None:
            options["color"] = colors
        options.update(kwargs)
        super().set_data(positions, **options)


class CircularGridLinesVisual(CirclesVisual):
    def set_data(self, radii, **kwargs):
        radii = numpy.reshape(radii, [-1])
        n_radii = radii.shape[0]
        centers = numpy.zeros([n_radii, 3])
        super().set_data(centers, radii, **kwargs)

    def set_default_data(self, **kwargs):
        radii_spacing = 10
        radius_ub = 1000
        n_radii = int(radius_ub / radii_spacing)
        radii = radii_spacing * numpy.arange(n_radii)[:, numpy.newaxis]
        n_theta = 100

        step_10 = int(numpy.around(10 / radii_spacing))
        step_100 = int(numpy.around(100 / radii_spacing))

        colors = numpy.ones([n_radii, 4])
        colors[:, :3] = 0.15
        colors[step_10::step_10, :3] = 0.3
        colors[step_100::step_100, :3] = 1

        options = {
            "colors": colors,
            "n_theta": n_theta,
        }
        options.update(**kwargs)
        self.set_data(radii, **options)


# class CircularGridMarkersVisual(TextVisual):
#     def set_data(self, radii, thetas, size=10, color=numpy.ones([4]), **kwargs):
#         self.clear()

#         pad = 0.5
#         for radius in radii:
#             for theta in thetas:
#                 position = numpy.zeros([2])
#                 position[0] = (radius + pad) * numpy.cos(theta)
#                 position[1] = (radius + pad) * numpy.sin(theta)
#                 options = {
#                     "bold": True,
#                     "color": color,
#                     "font_size": size,
#                     "pos": position,
#                     "text": "{}m".format(radius),
#                 }
#                 options.update(**kwargs)
#                 sub_visual = vispy.scene.visuals.Text(**options)
#                 self._sub_visuals.append(sub_visual)
#                 self.visual.add_subvisual(sub_visual)

#     def set_default_data(self, **kwargs):
#         radii = numpy.arange(100, 1000, 100)
#         thetas = numpy.radians([90])
#         self.set_data(radii, thetas, **kwargs)


class GridVisual:
    def __init__(self):
        self.visual = vispy.scene.visuals.Compound([])

        self._lines_visual = CircularGridLinesVisual()
        self._lines_visual.set_default_data()
        self.visual.add_subvisual(self._lines_visual.visual)


class STLMeshVisual(MeshVisual):
    def __init__(self, **kwargs):
        options = {
            "shading": "flat",
        }
        options.update(**kwargs)
        super().__init__(**options)
        self._visual.light_dir = (0, 0, 1)
        self._visual.shininess = 0

    def set_data(self, mesh_path, mesh_scale=1, mesh_transform=None, **kwargs):
        self._visual.visible = True

        # Load
        mesh = stl.mesh.Mesh.from_file(mesh_path)
        vertices = mesh.vectors.astype(float).reshape([-1, 3])
        faces = numpy.arange(vertices.shape[0]).reshape([-1, 3])

        # Transform
        vertices *= mesh_scale
        if mesh_transform is not None:
            vertices = mesh_transform.apply(vertices)

        options = {
            "faces": faces,
            "vertices": vertices,
        }
        options.update(**kwargs)
        self._visual.set_data(**options)


def get_meshes_path():
    cepton_alg_path = cepton_util.common.get_package_path("cepton_alg")
    return os.path.join(cepton_alg_path, "common/meshes")


def get_mesh_path(name):
    return os.path.join(get_meshes_path(), name)


class CarVisual(STLMeshVisual):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        mesh_path = get_mesh_path("car.stl")
        mesh_transform = cepton_alg.common.transform.Transform3d()
        mesh_transform.rotation.v[0, :] = [0, numpy.sqrt(0.5), numpy.sqrt(0.5)]
        mesh_transform.rotation.s[0] = 0
        options = {
            "color": 0.8 * numpy.ones(3),
            "mesh_scale": 0.02,
            "mesh_transform": mesh_transform,
        }
        options.update(kwargs)
        self.set_data(mesh_path, **options)


def get_selected_point(line, positions, threshold=1):
    n = positions.shape[0]
    if n == 0:
        return None

    d = vector_dot(positions - line.position, line.direction)
    projected_positions = line.position + d[:, numpy.newaxis] * line.direction
    distances = vector_norm(positions - projected_positions)
    idx = numpy.argmin(distances)
    if distances[idx] > threshold:
        return None
    return idx


# class RectangleSelector(InteractiveWidget):
#     def __init__(self, **kwargs):
#         self.lb = None
#         self.ub = None

#         super().__init__(**kwargs)

#         self.visual = vispy.scene.visuals.Compound([])

#         self.clear()

#     def clear(self):
#         self.lb = None
#         self.ub = None

#         self.

#     def _init_rectangle(self):


#     def on_mouse_press(self, event, view):
#         if not self.enabled:
#             return False
#         position = get_mouse_position(event, view)
#         if set(event.modifiers) == {vispy.util.keys.CONTROL}:
#             if event.button == 1:
#                 # Lower bound
#                 self.lb = position
#                 self.ub = position
#                 return True
#         return False

#     def on_mouse_move(self, event, view):
#         if not self.enabled:
#             return False


class PointsSelector(InteractiveWidget):
    def __init__(self, **kwargs):
        self._points = None
        self.update_callbacks = []
        # self.lb = numpy.full([3], -numpy.inf)
        # self.ub = numpy.full([3], numpy.inf)

        super().__init__(**kwargs)

        self.visual = vispy.scene.visuals.Compound([])
        self._positions_visual = MarkersVisual()
        self._bounds_visual = BoxesVisual()
        self.visual.add_subvisual(self._positions_visual.visual)

        self.clear()

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, values):
        self._points = values
        self.selected_indices = numpy.array([], dtype=int)
        self.update()

    @property
    def selected_points(self):
        if self.points is None:
            return None
        return self.points[self.selected_indices]

    def clear(self):
        self.selected_indices = numpy.array([], dtype=int)
        self.selected_position = numpy.zeros([3])

        self._positions_visual.clear()

    def on_mouse_press(self, event, view):
        if not self.enabled:
            return False
        if self._points is None:
            return False
        line = get_mouse_event_line(event, view)
        if set(event.modifiers) == {vispy.util.keys.CONTROL}:
            if event.button == 1:
                # Select point
                idx = get_selected_point(line, self._points.positions)
                if idx is None:
                    self.clear()
                else:
                    self.selected_position[:] = self._points.positions[idx, :]
                    self.selected_indices = numpy.array([idx], dtype=int)
                self.update()
                for f in self.update_callbacks:
                    f()
                return True
        return False

    def update(self):
        if not self.enabled:
            return
        if (self.points is None) or (len(self.selected_indices) == 0):
            self.clear()
            return

        self._update_positions()

    def _update_positions(self):
        self._positions_visual.visible = True
        positions = self.points.positions[self.selected_indices, :]

        options = {
            "edge_width": 0,
            "face_color": "red",
            "pos": positions,
            "size": 15,
        }
        self._positions_visual.set_data(**options)


class PointsVisual(MarkersVisual, cepton_util.common.OptionsMixin):
    def get_options(self):
        options = super().get_options()
        options.update({
            "point_size": self.point_size,
        })
        return options

    def set_options(self, **kwargs):
        super().set_options(**kwargs)
        self.point_size = kwargs.get("point_size", 2)

    def set_data(self, positions, **kwargs):
        if len(positions) == 0:
            self.clear()
            return
        self._visual.visible = True

        options = {
            "edge_width": 0,
            "pos": positions,
            "size": self.point_size,
        }
        options.update(**kwargs)
        self._visual.set_data(**options)


class ColoredPointsVisual(PointsVisual):
    def get_options(self):
        options = super().get_options()
        options.update({
            "color_map": self.color_map.name,
            "color_min": self.color_min,
            "color_max": self.color_max,
            "color_scale": self.color_scale,
        })
        return options

    def set_options(self, **kwargs):
        super().set_options(**kwargs)
        self.color_map = cepton_util.parse_enum(
            kwargs.get("color_map", ColorMap.CONSTANT), ColorMap)
        self.color_min = kwargs.get("color_min", 0)
        if "color_max" in kwargs:
            self.color_max = kwargs.get("color_max", 1)
        else:
            self.color_scale = kwargs.get("color_scale", 1)

    @property
    def color_scale(self):
        return self.color_max - self.color_min

    @color_scale.setter
    def color_scale(self, value):
        self.color_max = self.color_min + value

    @property
    def color_lut(self):
        return get_color_lut(self.color_map)

    def get_colors(self, color_values, shading=None):
        color_lut = self.color_lut

        n = color_values.shape[0]
        is_valid = numpy.isfinite(color_values)
        color_values = color_values[is_valid]
        colors = numpy.ones([n, 4])
        if self.color_map is ColorMap.CATEGORICAL:
            colors[is_valid, :] = get_categorical_colors(
                color_values, color_lut)
        else:
            color_values = color_values / self.color_scale
            if self.color_map is ColorMap.CIRCULAR:
                # HACK
                # color_values = numpy.mod(color_values, 1)
                color_values = numpy.clip(color_values, 0, 1)
            else:
                color_values = numpy.clip(color_values, 0, 1)
            colors[is_valid, :] = get_colors(color_values, color_lut)
        if shading is not None:
            colors[:, :3] *= shading[:, numpy.newaxis]
        return colors

    def set_data(self, positions, color_values, shading=None, **kwargs):
        options = {
            "face_color": self.get_colors(color_values, shading=shading),
        }
        options.update(kwargs)
        super().set_data(positions, **options)


@enum.unique
class SDKPointColorMode(enum.IntEnum):
    CONSTANT = 0
    INTENSITY = 1
    Z = 2


class SDKPointsVisual(ColoredPointsVisual):
    @property
    def color_mode(self):
        return self._color_mode

    @color_mode.setter
    def color_mode(self, value):
        self._color_mode = value
        self.color_min = 0
        self.color_scale = {
            SDKPointColorMode.Z: 10,
        }.get(self._color_mode, 1.0)
        self.color_map = {
            SDKPointColorMode.INTENSITY: ColorMap.SEQUENTIAL,
            SDKPointColorMode.Z: ColorMap.CIRCULAR,
        }.get(self._color_mode, ColorMap.CONSTANT)

    @property
    def is_color_scale_constant(self):
        return {
            SDKPointColorMode.CONSTANT: True,
        }.get(self.color_mode, False)

    def get_options(self):
        options = super().get_options()
        options.update({
            "color_mode": self.color_mode.name,
        })
        return options

    def set_options(self, **kwargs):
        super().set_options(**kwargs)
        self.color_mode = cepton_util.common.parse_enum(kwargs.get(
            "color_mode", SDKPointColorMode.CONSTANT), SDKPointColorMode)
        if "color_scale" in kwargs:
            self.color_scale = kwargs["color_scale"]
        if "color_map" in kwargs:
            self.color_map = cepton_util.parse_enum(
                kwargs.get("color_map", ColorMap.CONSTANT), ColorMap)

    def get_color_values(self, points):
        color_values = numpy.full([len(points)], numpy.nan)
        if self.color_mode is SDKPointColorMode.INTENSITY:
            color_values[:] = points.intensities
        elif self.color_mode is SDKPointColorMode.Z:
            color_values[:] = points.positions[:, 2]
        return color_values

    def set_data(self, points, **kwargs):
        color_values = self.get_color_values(points)
        super().set_data(points.positions, color_values, **kwargs)


class VispyCamera(vispy.scene.cameras.turntable.TurntableCamera):
    def viewbox_mouse_event(self, event):
        # https://github.com/vispy/vispy/blob/master/vispy/scene/cameras/perspective.py
        if event.handled or not self.interactive:
            return

        if event.type == 'mouse_move':
            if event.press_event is None:
                return

            modifiers = event.mouse_event.modifiers
            p1 = event.mouse_event.press_event.pos
            p2 = event.mouse_event.pos
            d = p2 - p1

            if 2 in event.buttons and not modifiers:
                # Translate
                norm = numpy.mean(self._viewbox.size)
                if self._event_value is None or len(self._event_value) == 2:
                    self._event_value = self.center
                dist = (p1 - p2) / norm * self._scale_factor
                dist[1] *= -1
                # Black magic part 1: turn 2D into 3D translations
                dx, dy, dz = self._dist_to_trans(dist)
                # Black magic part 2: take up-vector and flipping into account
                ff = self._flip_factors
                up, forward, right = self._get_dim_vectors()
                dx, dy, dz = right * dx + forward * dy + up * dz
                dx, dy, dz = ff[0] * dx, ff[1] * dy, dz * ff[2]
                c = self._event_value
                self.center = c[0] + dx, c[1] + dy, c[2] + dz
                return

        super().viewbox_mouse_event(event)


class AbsoluteViewMotion:
    def __init__(self):
        self.camera = VispyCamera()
        self.t = numpy.zeros([1])
        self.interpolators = {}

    @property
    def t_max(self):
        return self.t[-1]

    def set_data(self, t_diff, data, mirror=False):
        if mirror:
            t_diff = numpy.concatenate([t_diff, t_diff[::-1]])
        t = numpy.zeros([len(t_diff) + 1])
        t[1:] = numpy.cumsum(t_diff)

        self.t = t
        t_step = 0.5
        t_fine = numpy.arange(numpy.amin(t), numpy.amax(t) + t_step, t_step)
        self.interpolators = {}
        for name, values in data.items():
            if mirror:
                values = numpy.concatenate([values, values[:-1][::-1]])

            # Refine values
            options = {
                "bounds_error": False,
                "fill_value": "extrapolate"
            }
            values_fine = \
                scipy.interpolate.interp1d(t, values, **options)(t_fine)

            options = {
                "kind": "cubic",
            }
            self.interpolators[name] = \
                scipy.interpolate.interp1d(t_fine, values_fine, **options)

    def get_absolute(self, t):
        t = numpy.mod(t, self.t_max)

        data = {}
        for name, interpolator in self.interpolators.items():
            data[name] = interpolator(t)
        return data

    def get(self, t):
        return self.get_absolute(t)

    def update(self, t):
        data = self.get(t)
        for name, value in data.items():
            setattr(self.camera, name, value)


class RelativeViewMotion(AbsoluteViewMotion):
    def __init__(self):
        self.previous_t = None

    def get(self, t):
        if self.previous_t is None:
            return {}

        t_diff = t - self.previous_t
        previous_data = super().get(self.previous_t)
        current_data = super().get(t)
        names = set(previous_data.keys()) & set(current_data.keys())
        data = {}
        for name in names:
            camera_value = getattr(self.camera, name)
            data[name] = \
                camera_value - previous_data[name] + current_data[name]
        return data

    def update(self, t):
        super().update(t)
        self.previous_t = t


class ViewMotionPan(RelativeViewMotion):
    def __init__(self, angle_min=0, angle_ptp=365, pan_speed=4):
        self.angle_min = angle_min
        self.angle_ptp = angle_ptp
        self.pan_speed = pan_speed

        super().__init__()

        angle_max = self.angle_min + self.direction * self.angle_ptp
        t_diff = [numpy.abs(self.angle_ptp / self.pan_speed)]
        data = {
            "azimuth": [self.angle_min, angle_max],
        }
        self.set_data(t_diff, data)

    @property
    def direction(self):
        return numpy.sign(self.pan_speed)


class ViewMotionPanSlow(ViewMotionPan):
    def __init__(self):
        options = {
            "pan_speed": 2,
        }
        super().__init__(**options)


class ViewMotionPanModerate(ViewMotionPan):
    def __init__(self):
        options = {
            "pan_speed": 4,
        }
        super().__init__(**options)


class ViewMotionPanFast(ViewMotionPan):
    def __init__(self):
        options = {
            "pan_speed": 8,
        }
        super().__init__(**options)


@enum.unique
class ViewMotionMode(enum.IntEnum):
    PAN_SLOW = 0
    PAN_MODERATE = 1
    PAN_FAST = 2


def create_view_motion(mode):
    return {
        ViewMotionMode.PAN_SLOW: ViewMotionPanSlow,
        ViewMotionMode.PAN_MODERATE: ViewMotionPanModerate,
        ViewMotionMode.PAN_FAST: ViewMotionPanFast,
    }[mode]()


class Renderer(cepton_util.common.OptionsMixin):
    """Visualization renderer with Vispy.

    This is the virtual base class of the actual renderer.
    The implementation class should implement `update` and `refresh` method.
    See //cepton_alg/python/cepton_alg/renderer.py for example.

    Args:
        exporter: `Exporter`.
        view_motion: `ViewMotion`.

    Controls:
        SPACE: pause / resume
        SCROLL_UP, SCROLL_DOWN: zoom in and zoom out
        MOUSE DRAG: rotate camera.
        SHIFT + MOUSE DRAG: translate camera.
        `1`/`2`/`3`: switch to front/top/side viewpoint.
        `A`: Enable angle ruler visual measurement.
        `D`: Enable distance ruler visual measurement.
        `N`: next frame, mostly useful when not animated.
        `S`: Capture screen shot.
        `V`: Print out camera rotation information.
    """

    def update(self):
        for func in self.update_callbacks:
            func()
        return False

    def refresh(self):
        for func in self.refresh_callbacks:
            func()
        self.update_plots()

    def update_plots(self):
        self.distance_ruler.update()
        self.angle_ruler.update()

    def __init__(self, exporter=None, standalone=True):
        self._view_motion = None
        self._view_motion_mode = None
        self.animation_timer = None
        self.exporter = exporter
        self.interactive_widgets = []
        self.is_running = False
        self.refresh_callbacks = []
        self.standalone = standalone
        self.t = 0
        self.t_animation = 0
        self.update_callbacks = []

        self.init_canvas()
        self.init_view()
        self.init_events()
        self.init_plots()

    def get_canvas_options(self):
        return {
            "fullscreen": self.canvas.fullscreen,
            "size": self.canvas.size,
        }

    def set_canvas_options(self, **kwargs):
        self.canvas.fullscreen = kwargs.get("fullscreen", False)
        self.canvas.size = kwargs.get("size", [800, 600])

    def get_camera_options(self):
        return {
            "azimuth": self.camera.azimuth,
            "center": self.camera.center,
            "depth_value": self.camera.depth_value,
            "elevation": self.camera.elevation,
            "fov": numpy.degrees(self.camera.fov),
            "scale_factor": self.camera.scale_factor,
        }

    def set_camera_options(self, **kwargs):
        self.camera.azimuth = kwargs.get("azimuth", 0)
        self.camera.center = kwargs.get("center", [0, 0, 0])
        self.camera.elevation = kwargs.get("elevation", 0)
        self.camera.depth_value = kwargs.get("depth_value", 1e3)
        self.camera.elevation = kwargs.get("elevation", 0)
        self.camera.fov = numpy.radians(kwargs.get("fov", 0))
        self.camera.scale_factor = kwargs.get("scale_factor", 40)

    def get_options(self):
        options = {}
        options.update({
            "camera": self.get_camera_options(),
            "canvas": self.get_canvas_options(),
            "frame_rate": self.frame_rate,
            "static": self.static,
            "view_motion_mode": self.view_motion_mode,
        })
        return options

    def set_options(self, **kwargs):
        super().set_options(**kwargs)
        self.frame_rate = kwargs.get("frame_rate", 10)
        self.set_camera_options(**kwargs.get("camera", {}))
        if self.standalone:
            self.set_canvas_options(**kwargs.get("canvas", {}))
        self.static = kwargs.get("static", False)
        self.view_motion_mode = cepton_util.parse_enum(
            kwargs.get("view_motion_mode", None), ViewMotionMode)

    @property
    def camera(self):
        return self.view.camera

    @property
    def frame_rate(self):
        return 1 / self.period

    @frame_rate.setter
    def frame_rate(self, value):
        self.pause_animation()
        self.period = 1 / value

    @property
    def view_motion(self):
        return self._view_motion

    @view_motion.setter
    def view_motion(self, value):
        self._view_motion = value
        self._view_motion_mode = None
        if value is None:
            return
        self._view_motion.camera = self.camera

    @property
    def view_motion_mode(self):
        return self._view_motion_mode

    @view_motion_mode.setter
    def view_motion_mode(self, value):
        if value is None:
            self.view_motion = None
            return
        self.view_motion = create_view_motion(value)
        self._view_motion_mode = value

    @property
    def angle_ruler_enabled(self):
        return self.angle_ruler.enabled

    @angle_ruler_enabled.setter
    def angle_ruler_enabled(self, value):
        if value:
            self.disable_interactive_widgets()
        self.angle_ruler.enabled = value
        self.refresh()

    @property
    def distance_ruler_enabled(self):
        return self.distance_ruler.enabled

    @distance_ruler_enabled.setter
    def distance_ruler_enabled(self, value):
        if value:
            self.disable_interactive_widgets()
        self.distance_ruler.enabled = value
        self.refresh()

    def add_visual(self, visual):
        # TODO: transforms don't work with subvisuals
        self.view.add(visual)
        # self.visual.add_subvisual(visual)

    def add_interactive_widget(self, widget):
        self.interactive_widgets.append(widget)

    def disable_interactive_widgets(self):
        for widget in self.interactive_widgets:
            widget.enabled = False

    def init_canvas(self):
        options = {}
        if self.standalone:
            options.update({
                "keys": "interactive",
                "position": [0, 0],
            })
        else:
            options.update({
                "keys": None,
            })
        self.canvas = vispy.scene.SceneCanvas(**options)

    def init_view(self):
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = VispyCamera()
        self.visual = vispy.scene.visuals.Compound([])
        self.view.add(self.visual)

    def init_events(self):
        self.canvas.connect(self.on_key_press)
        self.canvas.connect(self.on_mouse_move)
        self.canvas.connect(self.on_mouse_release)
        self.canvas.connect(self.on_mouse_press)
        self.canvas.connect(self.on_mouse_wheel)

    def init_plots(self):
        self.distance_ruler = DistanceRuler()
        self.add_visual(self.distance_ruler.visual)
        self.add_interactive_widget(self.distance_ruler)

        self.angle_ruler = AngleRuler()
        self.add_visual(self.angle_ruler.visual)
        self.add_interactive_widget(self.angle_ruler)

    def update_animation(self):
        if self.view_motion is not None:
            self.view_motion.update(self.t_animation)
        if not self.update():
            return
        self.t_animation += self.period
        if not self.static:
            self.t += self.period

    def run_once(self):
        self.update_animation()

    def run(self):
        self.canvas.show()
        self.run_once()
        vispy.app.run()

    def resume_animation(self):
        if self.is_running:
            return
        self.is_running = True

        def on_animation(*args):
            self.run_once()
        options = {
            "connect": on_animation,
            "interval": 1 / self.frame_rate,
            "start": True,
        }
        self.animation_timer = vispy.app.Timer(**options)

    def pause_animation(self):
        if not self.is_running:
            return
        self.is_running = False
        self.animation_timer.stop()

    def save_frame(self, **kwargs):
        if self.exporter:
            frame = self.canvas.render()
            self.exporter.save_frame(frame, **kwargs)

    def set_view_front(self):
        self.camera.azimuth = 0.0
        self.camera.elevation = 0.0

    def set_view_top(self):
        self.camera.azimuth = 0.0
        self.camera.elevation = 90.0

    def set_view_side(self):
        self.camera.azimuth = 90.0
        self.camera.elevation = 0.0

    def save_screenshot(self, path=None):
        if path is None:
            timestamp_str = cepton_util.common.get_timestamp_str()
            path = cepton_util.common.fix_path(
                "~/Pictures/cepton_{}.png".format(timestamp_str))
        frame = self.canvas.render()
        imageio.imwrite(path, frame)

    def on_key_press(self, event):
        for widget in self.interactive_widgets:
            if widget.on_key_press(event):
                return True
        if event.key == vispy.util.keys.SPACE:
            if self.is_running:
                self.pause_animation()
            else:
                self.resume_animation()
        elif event.key == "1":
            self.set_view_front()
            return True
        elif event.key == "2":
            self.set_view_top()
            return True
        elif event.key == "3":
            self.set_view_side()
            return True
        elif event.key == "A":
            self.angle_ruler_enabled = not self.angle_ruler_enabled
            return True
        elif event.key == "D":
            self.distance_ruler_enabled = not self.distance_ruler_enabled
            return True
        elif event.key == "N":
            self.run_once()
            return True
        elif event.key == "R":
            self.refresh()
            return True
        return False

    def on_mouse_press(self, event):
        for widget in self.interactive_widgets:
            if widget.on_mouse_press(event, self.view):
                return True
        return False

    def on_mouse_release(self, event):
        for widget in self.interactive_widgets:
            if widget.on_mouse_release(event, self.view):
                return True
        return False

    def on_mouse_move(self, event):
        for widget in self.interactive_widgets:
            if widget.on_mouse_move(event, self.view):
                return True
        return False

    def on_mouse_wheel(self, event):
        return False

    @property
    def camera_rotation(self):
        azimuth_tmp = numpy.radians(self.camera.azimuth)
        elevation_tmp = numpy.radians(self.camera.elevation)
        q = transforms3d.euler.euler2quat(
            -azimuth_tmp, elevation_tmp, 0, "szxy")
        return cepton_alg.common.transform.Quaternion.from_vector(
            q, scalar_first=True)


class PointsRenderer(Renderer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.car_visual = CarVisual()
        self.add_visual(self.car_visual.visual)

        self.grid_visual = GridVisual()
        self.add_visual(self.grid_visual.visual)

    def get_options(self):
        options = super().get_options()
        options.update({
            "mirror": self.mirror,
            "show_car": self.show_car,
            "show_grid": self.show_grid,
        })
        return options

    def set_options(self, **kwargs):
        super().set_options(**kwargs)
        self.mirror = kwargs.get("mirror", False)
        self.show_car = kwargs.get("show_car", False)
        self.show_grid = kwargs.get("show_grid", True)

    @property
    def mirror(self):
        return self.camera.flip == (True, False, False)

    @mirror.setter
    def mirror(self, value):
        if value:
            self.camera.flip = (True, False, False)
        else:
            self.camera.flip = (False, False, False)

    @property
    def show_car(self):
        return self.car_visual.visual.visible

    @show_car.setter
    def show_car(self, value):
        self.car_visual.visual.visible = value

    @property
    def show_grid(self):
        return self.grid_visual.visual.visible

    @show_grid.setter
    def show_grid(self, value):
        self.grid_visual.visual.visible = value


__all__ = _all_builder.get()
