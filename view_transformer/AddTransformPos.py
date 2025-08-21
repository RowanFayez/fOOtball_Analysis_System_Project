import numpy as np

class AddTransformPos:
	def __init__(self, transformer):
		"""transformer: instance providing transform_point(point) -> transformed coords or None"""
		self.transformer = transformer

	def add_transformed_position_to_tracks(self, tracks):
		for object, object_tracks in tracks.items():
			for frame_num, track in enumerate(object_tracks):
				for track_id, track_info in track.items():
					position = track_info.get('position_adjusted')
					if position is None:
						tracks[object][frame_num][track_id]['position_transformed'] = None
						continue
					position = np.array(position)
					position_transformed = self.transformer.transform_point(position)
					if position_transformed is not None:
						position_transformed = position_transformed.squeeze().tolist()
					tracks[object][frame_num][track_id]['position_transformed'] = position_transformed
