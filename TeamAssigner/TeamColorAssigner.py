from sklearn.cluster import KMeans

class TeamColorAssigner:
    def __init__(self):
        self.team_colors = {}
        self.kmeans = None

    def assign_team_color(self, frame, player_detections, color_extractor):
        
        player_colors = []
        for _, player_detection in player_detections.items():
            bbox = player_detection["bbox"]
            player_color = color_extractor.get_player_color(frame, bbox)
            player_colors.append(player_color)
        
        if len(player_colors) < 2:
            return  
        
        kmeans = KMeans(n_clusters=2, init="k-means++", n_init=10)
        kmeans.fit(player_colors)

        self.kmeans = kmeans

        self.team_colors[1] = kmeans.cluster_centers_[0]
        self.team_colors[2] = kmeans.cluster_centers_[1]