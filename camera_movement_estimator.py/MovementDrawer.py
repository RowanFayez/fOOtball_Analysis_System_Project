import cv2


class CameraMovementDrawer:
	def __init__(self):
		pass

	def draw_camera_movement(self, frames, camera_movement_per_frame):
		output_frames = []

		for frame_num, frame in enumerate(frames):
			frame = frame.copy()

			overlay = frame.copy()
			cv2.rectangle(overlay, (0, 0), (500, 100), (255, 255, 255), -1)
			alpha = 0.6
			cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

			x_movement, y_movement = camera_movement_per_frame[frame_num]
			frame = cv2.putText(frame, f"Camera Movement X: {x_movement:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
								(0, 0, 0), 3)
			frame = cv2.putText(frame, f"Camera Movement Y: {y_movement:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
								(0, 0, 0), 3)

			output_frames.append(frame)

		return output_frames

