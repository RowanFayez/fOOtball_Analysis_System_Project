from .TransformPointDetector import TransformPointDetector
from .AddTransformPos import AddTransformPos


class ViewTransformer:
    def __init__(self, pixel_vertices=None, target_vertices=None, court_width=68, court_length=23.32):
        # Compose specialized components
        self.detector = TransformPointDetector(pixel_vertices=pixel_vertices, target_vertices=target_vertices,
                                               court_width=court_width, court_length=court_length)
        self.adder = AddTransformPos(self.detector)

    def transform_point(self, point):
        return self.detector.transform_point(point)

    def add_transformed_position_to_tracks(self, tracks):
        return self.adder.add_transformed_position_to_tracks(tracks)
