from .SpeedAndDistanceAddition import SpeedAndDistanceAddition
from .SpeedAndDistanceDrawer import SpeedAndDistanceDrawer


class SpeedAndDistanceEstimator:
    def __init__(self, frame_window=5, frame_rate=24, distance_func=None):
        # Create the worker components
        self.adder = SpeedAndDistanceAddition(frame_window=frame_window, frame_rate=frame_rate, distance_func=distance_func)
        self.drawer = SpeedAndDistanceDrawer()

    def add_speed_and_distance_to_tracks(self, tracks):
        return self.adder.add_speed_and_distance_to_tracks(tracks)

    def draw_speed_and_distance(self, frames, tracks):
        return self.drawer.draw_speed_and_distance(frames, tracks)