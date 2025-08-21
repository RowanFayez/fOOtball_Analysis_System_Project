class PlayerTeamPredictor:
    def __init__(self):
        self.player_team_dict = {}

    def get_player_team(self,frame,player_bbox,player_id, color_extractor, team_color_assigner):
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]

        player_color = color_extractor.get_player_color(frame,player_bbox)

        team_id = team_color_assigner.kmeans.predict(player_color.reshape(1,-1))[0]
        team_id+=1

        if player_id ==91:
            team_id=1

        self.player_team_dict[player_id] = team_id

        return team_id
