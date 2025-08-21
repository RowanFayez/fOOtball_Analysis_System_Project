from .AnnotationDrawer import AnnotationDrawer
from.ObjectDetector import ObjectDetector
from .ObjectTracker import ObjectTracker
import pandas as pd

class Tracker:
    def __init__(self, model_path):
        self.detector = ObjectDetector(model_path)
        self.tracker = ObjectTracker()
        self.drawer = AnnotationDrawer()

    def detect_frames(self, frames):
        return self.detector.detect_frames(frames)

    def get_object_tracks(self, frames):
        detections = self.detect_frames(frames)
        return self.tracker.get_object_tracks(frames, detections)
    
    def draw_ellipse(self,frame,bbox,color,track_id=None):
        return self.drawer.draw_ellipse(frame,bbox,color,track_id)

    def draw_traingle(self,frame,bbox,color):
        return self.drawer.draw_traingle(frame,bbox,color)

    def draw_annotations(self,video_frames, tracks,team_ball_control):
        return self.drawer.draw_annotations(video_frames, tracks,team_ball_control)


    def interpolate_ball_positions(self, ball_positions):
        ball_positions = [x.get(1, {}).get("bbox", []) for x in ball_positions]

        df_ball_positions = pd.DataFrame(ball_positions)

        df_ball_positions = df_ball_positions.interpolate()
        df_ball_positions = df_ball_positions.bfill()

        ball_positions = [{1:{"bbox":x}} for x in df_ball_positions.to_numpy().tolist()]

        return ball_positions