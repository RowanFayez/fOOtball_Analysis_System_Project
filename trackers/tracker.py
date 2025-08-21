from .AnnotationDrawer import AnnotationDrawer
from.ObjectDetector import ObjectDetector
from .ObjectTracker import ObjectTracker


class Tracker:
    def __init__(self, model_path):
        self.detector = ObjectDetector(model_path)
        self.tracker = ObjectTracker()
        self.drawer = AnnotationDrawer()

    def detect_frames(self, frames):
        return self.detector.detect_frames(frames)

    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        detections = self.detect_frames(frames)
        return self.tracker.get_object_tracks(frames, detections, read_from_stub, stub_path)
    
    def draw_ellipse(self,frame,bbox,color,track_id=None):
        return self.drawer.draw_ellipse(frame,bbox,color,track_id)

    def draw_traingle(self,frame,bbox,color):
        return self.drawer.draw_traingle(frame,bbox,color)

    def draw_annotations(self,video_frames, tracks,team_ball_control):
        return self.drawer.draw_annotations(video_frames, tracks,team_ball_control)