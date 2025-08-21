import numpy as np
import cv2


class TransformPointDetector:
	def __init__(self, pixel_vertices=None, target_vertices=None, court_width=68, court_length=23.32):
		if pixel_vertices is None:
			pixel_vertices = np.array([[110, 1035],
									   [265, 275],
									   [910, 260],
									   [1640, 915]])

		if target_vertices is None:
			target_vertices = np.array([
				[0, court_width],
				[0, 0],
				[court_length, 0],
				[court_length, court_width]
			])

		self.pixel_vertices = pixel_vertices.astype(np.float32)
		self.target_vertices = target_vertices.astype(np.float32)
		self.perspective_transformer = cv2.getPerspectiveTransform(self.pixel_vertices, self.target_vertices)

	def transform_point(self, point):
		p = (int(point[0]), int(point[1]))
		is_inside = cv2.pointPolygonTest(self.pixel_vertices, p, False) >= 0
		if not is_inside:
			return None

		reshaped_point = point.reshape(-1, 1, 2).astype(np.float32)
		transformed_point = cv2.perspectiveTransform(reshaped_point, self.perspective_transformer)
		return transformed_point.reshape(-1, 2)
