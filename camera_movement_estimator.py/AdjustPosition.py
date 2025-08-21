class AdjustPositionAddition:
	def __init__(self):
		pass

	def add_adjust_positions_to_tracks(self, tracks, camera_movement_per_frame):
		for object, object_tracks in tracks.items():
			for frame_num, track in enumerate(object_tracks):
				for track_id, track_info in track.items():
					position = track_info.get('position')
					if position is None:
						continue
					camera_movement = camera_movement_per_frame[frame_num]
					position_adjusted = (position[0] - camera_movement[0], position[1] - camera_movement[1])
					tracks[object][frame_num][track_id]['position_adjusted'] = position_adjusted

