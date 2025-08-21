from .MovementGetter import CameraMovementGetter
from .AdjustPosition import AdjustPositionAddition
from .MovementDrawer import CameraMovementDrawer


class CameraMovementEstimator:
    def __init__(self, first_frame):
        self.getter = CameraMovementGetter(first_frame)
        self.adjuster = AdjustPositionAddition()
        self.drawer = CameraMovementDrawer()

    def get_camera_movement(self, frames, read_from_stub=False, stub_path=None):
        return self.getter.get_camera_movement(frames, read_from_stub=read_from_stub, stub_path=stub_path)

    def add_adjust_positions_to_tracks(self, tracks, camera_movement_per_frame):
        return self.adjuster.add_adjust_positions_to_tracks(tracks, camera_movement_per_frame)

    def draw_camera_movement(self, frames, camera_movement_per_frame):
        return self.drawer.draw_camera_movement(frames, camera_movement_per_frame)