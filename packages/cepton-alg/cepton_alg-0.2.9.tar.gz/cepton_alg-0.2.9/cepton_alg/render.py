import copy
import enum
import queue
import warnings

import numpy

import cepton_alg.c
import cepton_alg.core
import cepton_alg.frame
import cepton_sdk
import cepton_sdk.c
import cepton_util.common
from cepton_alg.common import *

_all_builder = AllBuilder(__name__)

from cepton_alg.common.render_vispy import *  # noqa isort:skip
try:
    from cepton_alg.render_mask import *  # noqa isort:skip
except ModuleNotFoundError:
    pass


class ObjectLabelsVisual(TextVisual):
    def __init__(self, *args, **kwargs):
        options = {
            "bold": True,
            "color": "red",
            "font_size": 10,
        }
        options.update(kwargs)
        super().__init__(*args, **options)

    def set_data(self, objects, **kwargs):
        options = {
            "pos": objects.transforms.translation,
            "text": [str(x) for x in objects.labels],
        }
        options.update(kwargs)
        super().set_data(**options)


# class ObjectBoxesVisual(WireBoxesVisual):
# """Object boxes."""
#     def set_data(self, objects, **kwargs):
#         colors = numpy.ones([len(objects), 4])
#         colors[:, :3] = [1, 0, 0]
#         # colors[numpy.logical_not(objects.is_moving), :3] *= 0.25

#         options = {
#             "colors": colors,
#         }
#         options.update(kwargs)
#         super().set_data(objects.boxes, **options)


class ObjectBoxesVisual(MeshBoxesVisual):
    """Object rectangles."""

    def set_data(self, objects, **kwargs):
        boxes = cepton_alg.common.geometry.Box3d(len(objects.boxes))
        boxes.dimensions[:, :2] = objects.boxes.dimensions[:, :2]
        boxes.transform.translation[:, :2] = \
            objects.boxes.transform.translation[:, :2]

        colors = numpy.ones([len(objects), 4])
        colors[:, :3] = [0.5, 0, 0]

        options = {
            "colors": colors,
            "box_options": {
                "pad": [0.25, 0.25, 0],
            }
        }
        options.update(kwargs)
        super().set_data(boxes, **options)


class ObjectTrajectoriesVisual(LineVisual):
    def set_data(self, objects, **kwargs):
        objects = objects[objects.is_moving.astype(bool)]

        positions = objects.trajectories
        positions = numpy.insert(positions, 0, numpy.nan, axis=1)
        positions = positions.reshape([-1, 3])

        options = {
            "color": "red",
        }
        options.update(kwargs)
        super().set_data(positions, **options)


class SurfacesVisual(VectorsVisual):
    def set_data(self, surfaces, **kwargs):
        positions = surfaces.planes.position
        vectors = surfaces.planes.normal
        options = {
            "color": "red",
        }
        options.update(kwargs)
        super().set_data(positions, vectors, **options)


class ScanVisual(LineVisual):
    def set_data(self, points, **kwargs):
        sort_keys = [points.scanline_labels,
                     points.segment_indices, points.serial_numbers]
        sort_indices = numpy.lexsort(sort_keys)
        points = points[sort_indices]
        positions = points.positions

        color_values = points.scanline_labels
        color_lut = get_categorical_color_lut()
        colors = get_categorical_colors(color_values, color_lut)

        # Cut lines
        is_invalid = numpy.logical_or.reduce([
            numpy.abs(numpy.diff(points.serial_numbers)) > 0,
            numpy.abs(numpy.diff(points.segment_indices)) > 0,
            numpy.abs(numpy.diff(points.scanline_labels)) > 0,
            vector_norm(numpy.diff(
                points.positions, axis=0), axis=1) > 5,
        ])
        cuts = numpy.flatnonzero(is_invalid) + 1
        positions = numpy.insert(positions, cuts, numpy.nan, axis=0)
        colors = numpy.insert(colors, cuts, 0, axis=0)

        options = {
            "color": colors,
        }
        options.update(**kwargs)
        super().set_data(positions, **options)


FramePointColorMode = SDKPointColorMode


class FramePointsVisual(SDKPointsVisual):
    def set_data(self, frame, points, **kwargs):
        options = {
            "shading": points.shading,
        }
        options.update(kwargs)
        super().set_data(points, **options)


class AllPointsVisual(PointsVisual):
    def set_data(self, frame, points, selected_points_flag=None, **kwargs):
        colors = numpy.ones([len(points), 4])
        sizes = numpy.full([len(points)], 2)
        if selected_points_flag is not None:
            colors[:, :] = [1, 1, 1, 0.5]
            is_selected = points.get_flag(selected_points_flag)
            colors[is_selected, :] = [1, 0, 0, 1]
            sizes[is_selected] = 2 * self.point_size
        options = {
            "face_color": colors,
            "size": sizes,
        }
        options.update(kwargs)
        super().set_data(points.positions, **options)


class StationaryPointsVisual(PointsVisual):
    def set_data(self, frame, points, **kwargs):
        colors = numpy.ones([len(points), 4])
        colors[:, :] = [0.5, 0.5, 0.5, 0.5]
        colors[:, :3] *= points.shading[:, numpy.newaxis]

        options = {
            "face_color": colors,
        }
        options.update(kwargs)
        super().set_data(points.positions, **options)


class GroundPointsVisual(PointsVisual):
    def set_data(self, frame, points, **kwargs):
        colors = numpy.ones([len(points), 4])
        colors[:, :] = [0.5, 0.5, 0.5, 1]
        colors[:, :3] *= points.shading[:, numpy.newaxis]

        options = {
            "face_color": colors,
        }
        options.update(kwargs)
        super().set_data(points.positions, **options)


@enum.unique
class ObjectPointColorMode(enum.IntEnum):
    CONSTANT = 0
    OBJECT_LABEL = 1
    OBJECT_TYPE = 2


class ObjectPointsVisual(ColoredPointsVisual):
    @property
    def color_mode(self):
        return self._color_mode

    @color_mode.setter
    def color_mode(self, value):
        self._color_mode = value
        self.color_map = {
            ObjectPointColorMode.OBJECT_LABEL: ColorMap.CATEGORICAL,
            ObjectPointColorMode.OBJECT_TYPE: ColorMap.CATEGORICAL,
        }.get(self._color_mode, ColorMap.CONSTANT)

    def get_options(self):
        options = super().get_options()
        options.update({
            "color_mode": cepton_util.common.serialize_enum(self.color_mode),
        })
        return options

    def set_options(self, **kwargs):
        super().set_options(**kwargs)
        self.color_mode = cepton_util.common.parse_enum(kwargs.get(
            "color_mode", ObjectPointColorMode.CONSTANT), ObjectPointColorMode)

    def get_color_values(self, frame, points):
        objects = frame.objects
        color_values = numpy.full([len(points)], numpy.nan)
        if self.color_mode is ObjectPointColorMode.OBJECT_LABEL:
            color_values[:] = objects.labels[points.object_indices]
        elif self.color_mode is ObjectPointColorMode.OBJECT_TYPE:
            color_values[:] = objects.types[points.object_indices]
        return color_values

    def set_data(self, frame, points, **kwargs):
        objects = frame.objects

        color_values = self.get_color_values(frame, points)
        shading = points.shading

        # is_moving = objects.is_moving[points.object_indices].astype(bool)
        # shading[numpy.logical_not(is_moving)] *= 0.5

        options = {
            "shading": shading,
        }
        options.update(kwargs)
        super().set_data(points.positions, color_values, **options)


class CoordinateReference(enum.IntEnum):
    DEFAULT = 0
    GROUND = 1
    CEILING = 2


class FrameRenderer(PointsRenderer):
    def __init__(self, **kwargs):
        if cepton_alg.advanced():
            self._active_image_mask_editor_id = None
            self._active_mask_editor_id = None
        self._alg_options = None
        self._frame_accumulator = cepton_alg.frame.SimpleFrameAccumulator()
        self._new_frames = queue.Queue(maxsize=10)

        super().__init__(**kwargs)

    @property
    def alg_options(self):
        if self._alg_options is None:
            if not cepton_alg.is_initialized():
                warnings.warn("Not started!", RuntimeWarning)
                return {}
            self._alg_options = cepton_alg.get_options()
        return self._alg_options

    @property
    def enable_indoor(self):
        return self.alg_options.get("enable_indoor", False)

    @property
    def is_realtime(self):
        return cepton_sdk.is_live()

    @property
    def fast(self):
        if self.is_realtime:
            return True
        return self._fast

    @fast.setter
    def fast(self, value):
        self._fast = value

    @property
    def show_scan(self):
        return self.scan_visual.visible

    @show_scan.setter
    def show_scan(self, value):
        self.scan_visual.visible = value

    @property
    def show_object_labels(self):
        return self.object_labels_visual.visible

    @show_object_labels.setter
    def show_object_labels(self, value):
        self.object_labels_visual.visible = value

    @property
    def show_object_boxes(self):
        return self.object_boxes_visual.visible

    @show_object_boxes.setter
    def show_object_boxes(self, value):
        self.object_boxes_visual.visible = value

    @property
    def show_object_trajectories(self):
        return self.object_trajectories_visual.visible

    @show_object_trajectories.setter
    def show_object_trajectories(self, value):
        self.object_trajectories_visual.visible = value

    @property
    def show_surfaces(self):
        return self.surfaces_visual.visible

    @show_surfaces.setter
    def show_surfaces(self, value):
        self.surfaces_visual.visible = value

    @property
    def show_occupancy(self):
        return self.grid_occupancy_visual.visible

    @show_occupancy.setter
    def show_occupancy(self, value):
        self.grid_occupancy_visual.visible = value

    def disable_image_mask_editors(self):
        for editor in self.image_mask_editors.values():
            editor.enabled = False

    @property
    def active_image_mask_editor_id(self):
        return self._active_image_mask_editor_id

    @active_image_mask_editor_id.setter
    def active_image_mask_editor_id(self, value):
        if self._active_image_mask_editor_id == value:
            return
        self.disable_image_mask_editors()
        self._active_image_mask_editor_id = value
        if value is not None:
            self.disable_interactive_widgets()
            self.active_mask_editor_id = None
            editor = self.image_mask_editors[value]
            editor.enabled = True

    @property
    def active_image_mask_editor(self):
        if self.active_image_mask_editor_id is None:
            return None
        return self.image_mask_editors[self.active_image_mask_editor_id]

    def disable_mask_editors(self):
        for editor in self.mask_editors.values():
            editor.enabled = False

    @property
    def active_mask_editor_id(self):
        return self._active_mask_editor_id

    @active_mask_editor_id.setter
    def active_mask_editor_id(self, value):
        if self._active_mask_editor_id == value:
            return
        self.disable_mask_editors()
        self._active_mask_editor_id = value
        if value is not None:
            self.active_image_mask_editor_id = None
            editor = self.mask_editors[value]
            editor.enabled = True

    @property
    def active_mask_editor(self):
        if self.active_mask_editor_id is None:
            return None
        return self.mask_editors[self.active_mask_editor_id]

    @property
    def points_selector_enabled(self):
        return self.points_selector.enabled

    @points_selector_enabled.setter
    def points_selector_enabled(self, value):
        if value:
            self.disable_interactive_widgets()
        self.points_selector.enabled = value
        self.refresh()

    def get_options(self):
        options = super().get_options()
        options.update({
            "coordinate_reference": cepton_util.common.serialize_enum(
                self.coordinate_reference),
            "downsample_ground": self.downsample_ground,
            "enable_shading": self.enable_shading,
            "fast": self.fast,
            "frame_length": self.frame_length,
            "interpolate_frames": self.interpolate_frames,
            "object_points_visual": self.object_points_visual.get_options(),
            "point_size": self.point_size,
            "points_visual": self.points_visual.get_options(),
            "selected_points_flag": cepton_util.common.serialize_enum(
                self.selected_points_flag),
            "show_all_objects": self.show_all_objects,
            "show_all_points": self.show_all_points,
            "show_object_boxes": self.show_object_boxes,
            "show_object_labels": self.show_object_labels,
            "show_object_trajectories": self.show_object_trajectories,
            "show_occupancy": self.show_occupancy,
            "show_scan": self.show_scan,
            "show_surfaces": self.show_surfaces,
        })
        return options

    def set_options(self, **kwargs):
        super().set_options(**kwargs)
        self.coordinate_reference = cepton_util.common.parse_enum(
            kwargs.get("coordinate_reference", CoordinateReference.DEFAULT),
            CoordinateReference)
        self.downsample_ground = kwargs.get("downsample_ground", True)
        self.enable_shading = kwargs.get("enable_shading", False)
        self.fast = kwargs.get("fast", True)
        self.frame_length = kwargs.get("frame_length", 0.1)
        self.interpolate_frames = kwargs.get("interpolate_frames", False)
        self.object_points_visual.set_options(
            **kwargs.get("object_points_visual", {}))
        self.point_size = kwargs.get("point_size", 2)
        self.points_visual.set_options(**kwargs.get("points_visual", {}))
        self.selected_points_flag = cepton_util.common.parse_enum(
            kwargs.get("selected_points_flag", None),
            cepton_alg.CombinedPointFlag)
        self.show_all_objects = kwargs.get("show_all_objects", False)
        self.show_all_points = kwargs.get("show_all_points", False)
        self.show_object_boxes = kwargs.get("show_object_boxes", True)
        self.show_object_labels = kwargs.get("show_object_labels", False)
        self.show_object_trajectories = kwargs.get(
            "show_object_trajectories", True)
        self.show_occupancy = kwargs.get("show_occupancy", False)
        self.show_scan = kwargs.get("show_scan", False)
        self.show_surfaces = kwargs.get("show_surfaces", False)

    @property
    def coordinate_transform(self):
        if self.coordinate_reference is CoordinateReference.DEFAULT:
            return cepton_alg.common.transform.Transform3d()
        plane = {
            CoordinateReference.GROUND: self.frame.ground_plane,
            CoordinateReference.CEILING: self.frame.ceiling_plane,
        }[self.coordinate_reference]
        return cepton_alg.common.geometry.compute_ground_transform(plane)

    def clear(self):
        super().clear()

        clear_queue(self._new_frames)
        self._alg_options = None
        self.timestamp_0 = None
        self.timestamp = None
        self.frame = None
        self._frame_accumulator.clear()

        self.clear_frame_plots()

    def process_frame(self, frame):
        # HACK
        is_valid = frame.points.positions[:, 2] < 10
        frame.points = frame.points[is_valid]

        pass

    def add_frame(self, frame):
        if cepton_sdk.capture_replay.is_running():
            if cepton_alg.core.is_full() or (self._new_frames.qsize() > 4):
                cepton_sdk.capture_replay.pause()

        if self.is_realtime:
            clear_queue(self._new_frames)
        try:
            self._new_frames.put_nowait(frame)
        except queue.Full:
            warnings.warn("Frame queue full!")
            clear_queue(self._new_frames)

    def resume_animation(self):
        if not cepton_alg.is_initialized():
            warnings.warn("Not started!", RuntimeWarning)
            return
        if self.is_running:
            return
        if cepton_sdk.is_live():
            cepton_sdk.disable_control_flags(
                cepton_sdk.ControlFlag.DISABLE_NETWORK)
        super().resume_animation()

    def pause_animation(self):
        if not self.is_running:
            return
        cepton_sdk.enable_control_flags(
            cepton_sdk.ControlFlag.DISABLE_NETWORK)
        super().pause_animation()

    def update(self):
        super().update()

        if cepton_sdk.capture_replay.is_open() and \
                (not cepton_sdk.capture_replay.is_running()) and \
                (self._new_frames.qsize() < 2) and \
                (not cepton_alg.core.is_full()):
            cepton_sdk.capture_replay.resume()
        if self.fast:
            try:
                frame = self._new_frames.get_nowait()
            except queue.Empty:
                return False
            self.process_frame(frame)
            self.frame = frame
            self.timestamp = numpy.amax(self.frame.points.timestamps)
        else:
            # TODO
            # if self.timestamp is not None:
            #     # Check for timestamp jump
            #     t_offset = self.timestamp - self._frame_accumulator.timestamp_max
            #     t_offset :
            #     self.timestamp_0 = None
            #     self.timestamp = None
            if (self.timestamp_0 is None) or (not self._frame_accumulator.has_frame(self.t + self.timestamp_0)):
                try:
                    frame = self._new_frames.get_nowait()
                except queue.Empty:
                    return False
                self.process_frame(frame)
                if self.timestamp_0 is None:
                    self.timestamp_0 = frame.timestamp - self.t
                self._frame_accumulator.add_frame(frame)

            timestamp_tmp = self.t + self.timestamp_0
            if not self._frame_accumulator.has_frame(timestamp_tmp):
                return False
            self.timestamp = timestamp_tmp

        self.refresh()
        return True

    def refresh(self):
        super().refresh()

        # HACK
        relative = True

        # Update frame
        if self.fast:
            frame = copy.deepcopy(self.frame)
        else:
            if self.timestamp is None:
                return
            options = {
                "frame_length": self.frame_length,
                "interpolate": self.interpolate_frames,
                "relative": relative,
                "timestamp": self.timestamp,
            }
            self.frame = self._frame_accumulator.get_frame(**options)
            frame = copy.deepcopy(self.frame)
        if frame is None:
            return
        self.prepare_frame(frame)
        self.update_frame_plots(frame)

        # HACK
        if not relative:
            transform = frame.motion_state.transform
            transform_mat = transform.to_matrix()[0, :, :]
            transform = vispy.visuals.transforms.MatrixTransform(
                transform_mat.transpose())
            self.car_visual.transform = transform
            self.grid_visual.transform = transform

    def prepare_frame(self, frame):
        if self.enable_shading and (not self.fast):
            is_valid_list = [
                frame.points.is_filtered,
                frame.points.is_ground,
            ]
            if not self.enable_indoor:
                is_valid_list.append(frame.points.is_stationary)
            is_valid = numpy.logical_or.reduce(is_valid_list)
            frame.points.shading[is_valid] = self.compute_shading(
                frame.points[is_valid])

        # HACK
        # distances = vector_norm(frame.points.positions[:, :2])
        # clip_radius = 10 + 10 * self.t_animation
        # is_invalid = distances > clip_radius
        # frame.points.shading[is_invalid] = 0

        if self.coordinate_reference is not CoordinateReference.DEFAULT:
            frame.points.positions[:, :] = self.coordinate_transform.apply(
                frame.points.positions)

    def update_plots(self):
        super().update_plots()

        if cepton_alg.advanced():
            for editor in self.image_mask_editors.values():
                editor.update()

    def update_frame_plots(self, frame):
        self.clear_frame_plots()

        if self.show_scan:
            self.update_scan(frame)

        if len(frame.points) > 0:
            if self.show_all_points or (self.selected_points_flag is not None):
                self.all_points_visual.set_data(
                    frame, frame.points, selected_points_flag=self.selected_points_flag)
            else:
                self.update_points(frame)

        self.update_objects(frame)
        self.update_surfaces(frame)
        if self.show_occupancy:
            self.update_occupancy(frame)

        self.points_selector.points = self.frame.points

        if cepton_alg.advanced():
            self.update_grid_mask_editors(frame)

    def init_plots(self):
        super().init_plots()

        self.scan_visual = ScanVisual()
        self.add_visual(self.scan_visual)

        self.all_points_visual = AllPointsVisual()
        self.add_visual(self.all_points_visual)

        self.points_visual = FramePointsVisual()
        self.add_visual(self.points_visual)

        self.stationary_points_visual = StationaryPointsVisual()
        self.add_visual(self.stationary_points_visual)

        self.ground_points_visual = GroundPointsVisual()
        self.add_visual(self.ground_points_visual)

        self.object_points_visual = ObjectPointsVisual()
        self.add_visual(self.object_points_visual)

        self.object_labels_visual = ObjectLabelsVisual()
        self.add_visual(self.object_labels_visual)

        self.object_boxes_visual = ObjectBoxesVisual()
        self.add_visual(self.object_boxes_visual)

        self.object_trajectories_visual = ObjectTrajectoriesVisual()
        self.add_visual(self.object_trajectories_visual)

        self.surfaces_visual = SurfacesVisual()
        self.add_visual(self.surfaces_visual)

        self.points_selector = PointsSelector()
        self.add_visual(self.points_selector.visual)
        self.add_interactive_widget(self.points_selector)

        self.grid_occupancy_visual = BinaryGridImageVisual()
        self.add_visual(self.grid_occupancy_visual)

        if cepton_alg.advanced():
            self.image_mask_editors = {}
            GridMaskId = cepton_alg.core.GridMaskId
            for mask_id in [GridMaskId.ABSOLUTE_2D, GridMaskId.RELATIVE_2D]:
                editor = GridImageMaskEditor(mask_id)
                self.add_visual(editor.visual)
                self.add_visual(editor.mask_visual)
                self.add_interactive_widget(editor)
                self.image_mask_editors[mask_id] = editor

            self.mask_editors = {}
            for mask_id in [GridMaskId.ABSOLUTE_3D, GridMaskId.RELATIVE_3D]:
                editor = GridMaskEditor(mask_id)
                self.add_visual(editor.mask_visual)
                self.mask_editors[mask_id] = editor

    def clear_frame_plots(self):
        self.scan_visual.clear()

        self.all_points_visual.clear()
        self.points_visual.clear()
        self.stationary_points_visual.clear()
        self.ground_points_visual.clear()
        self.object_points_visual.clear()

        self.object_labels_visual.clear()
        self.object_boxes_visual.clear()
        self.object_trajectories_visual.clear()

        self.surfaces_visual.clear()

        self.points_selector.visual.clear()
        self.grid_occupancy_visual.clear()

    def compute_shading(self, points):
        if len(points) == 0:
            return
        positions = self.camera_rotation.apply(points.positions)
        image_positions = positions[:, [0, 2]] * 10
        distances = positions[:, 1] / 3
        # TODO: fade out past 50m
        return cepton_alg.c.compute_shading(image_positions, distances)

    def update_scan(self, frame):
        points = frame.points
        if not self.show_all_points:
            points = points[points.is_filtered]
        if len(points) == 0:
            return
        self.scan_visual.set_data(points)

    def update_all_points(self, frame, points):
        if len(points) == 0:
            return

    def update_points(self, frame):
        points = frame.points

        self.points_visual.point_size = self.point_size
        self.object_points_visual.point_size = 1.5 * self.point_size
        self.all_points_visual.point_size = 0.5 * self.point_size
        self.stationary_points_visual.point_size = 0.5 * self.point_size
        self.ground_points_visual.point_size = 0.5 * self.point_size

        is_ground = numpy.logical_or.reduce([
            frame.points.is_ground,
            frame.points.is_ceiling,
        ])
        ground_points = points[is_ground]
        points = points[numpy.logical_not(is_ground)]
        if self.downsample_ground:
            ground_points = ground_points[ground_points.is_downsampled_coarse]
        if len(ground_points) > 0:
            self.ground_points_visual.set_data(frame, ground_points)

        points = points[points.is_downsampled_fine]

        is_stationary = points.is_stationary
        stationary_points = points[is_stationary]
        points = points[numpy.logical_not(is_stationary)]
        if self.enable_indoor:
            if len(stationary_points) > 0:
                self.stationary_points_visual.set_data(
                    frame, stationary_points)

        points = points[points.is_filtered]

        is_object = points.object_indices >= 0
        object_points = points[is_object]
        points = points[numpy.logical_not(is_object)]
        if not self.show_all_objects:
            is_valid_object = frame.objects.is_valid[object_points.object_indices]
            invalid_object_points = object_points[numpy.logical_not(
                is_valid_object)]
            object_points = object_points[is_valid_object]
        if len(object_points) > 0:
            self.object_points_visual.set_data(frame, object_points)

        is_valid = points.is_filtered
        points = points[is_valid]
        points_list = [points]
        if not self.enable_indoor:
            points_list.append(stationary_points)
        if not self.show_all_objects:
            points_list.append(invalid_object_points)
        points = cepton_sdk.combine_points(points_list)
        if len(points) > 0:
            self.points_visual.set_data(frame, points)

    def update_objects(self, frame):
        objects = frame.objects
        if not self.show_all_objects:
            objects = objects[objects.is_valid]
        if len(objects) == 0:
            return
        self.object_labels_visual.set_data(objects)
        self.object_boxes_visual.set_data(objects)
        self.object_trajectories_visual.set_data(objects)

    def update_surfaces(self, frame):
        if len(frame.surfaces) == 0:
            return
        self.surfaces_visual.set_data(frame.surfaces)

    def update_occupancy(self, frame):
        self.grid_occupancy_visual.set_data(
            frame.occupancy_grid, frame.occupancy_cells.is_valid)

    def update_grid_mask_editors(self, frame):
        transform = None
        for editor in self.image_mask_editors.values():
            if editor.mask_relative:
                continue
            if not editor.enabled:
                continue
            # Creating transform is expensive for some reason
            if transform is None:
                transform = frame.motion_state.transform.inverse()
                transform_mat = transform.to_matrix()[0, :, :]
                transform = vispy.visuals.transforms.MatrixTransform(
                    transform_mat.transpose())
            editor.transform = transform

    def on_key_press(self, event):
        if super().on_key_press(event):
            return True
        elif event.key == "S":
            self.points_selector_enabled = not self.points_selector_enabled
            return True
        return False


__all__ = _all_builder.get()
