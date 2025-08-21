from .ColorExtractor import ColorExtractor
from .TeamColorAssigner import TeamColorAssigner
from .PlayerTeamPredictor import PlayerTeamPredictor

class TeamAssigner:
    def __init__(self):
        self.team_colors = {}
        self.player_team_dict = {}
        self.color_extractor = ColorExtractor()
        self.team_color_assigner = TeamColorAssigner()
        self.player_team_predictor = PlayerTeamPredictor()
    
    def get_clustering_model(self,image):
        return self.color_extractor.get_clustering_model(image)

    def get_player_color(self,frame,bbox):
        return self.color_extractor.get_player_color(frame,bbox)

    def assign_team_color(self,frame, player_detections):
        self.team_color_assigner.assign_team_color(frame, player_detections, self.color_extractor)
        self.team_colors = self.team_color_assigner.team_colors

    def get_player_team(self,frame,player_bbox,player_id):
        team_id = self.player_team_predictor.get_player_team(frame,player_bbox,player_id, self.color_extractor, self.team_color_assigner)
        self.player_team_dict = self.player_team_predictor.player_team_dict
        return team_id