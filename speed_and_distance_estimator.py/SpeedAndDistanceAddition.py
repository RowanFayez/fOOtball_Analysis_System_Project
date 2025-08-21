from ..utils import measure_distance


class SpeedAndDistanceAddition:
    def __init__(self, frame_window=5, frame_rate=24, distance_func=None):
        """
        distance_func(start_pos, end_pos) -> distance in meters
        If distance_func is None, falls back to utils.measure_distance
        """
        self.frame_window = frame_window
        self.frame_rate = frame_rate
        self.distance_func = distance_func or measure_distance

    def add_speed_and_distance_to_tracks(self, tracks):
        total_distance = {}

        for obj, object_tracks in tracks.items():
            if obj in ("ball", "referees"):
                continue
            number_of_frames = len(object_tracks)
            for frame_num in range(0, number_of_frames, self.frame_window):
                last_frame = min(frame_num + self.frame_window, number_of_frames - 1)

                # iterate all track ids present in the start frame
                for track_id, _ in object_tracks[frame_num].items():
                    if track_id not in object_tracks[last_frame]:
                        continue

                    start_position = object_tracks[frame_num][track_id].get('position_transformed')
                    end_position = object_tracks[last_frame][track_id].get('position_transformed')

                    if start_position is None or end_position is None:
                        continue

                    distance_covered = self.distance_func(start_position, end_position)
                    time_elapsed = (last_frame - frame_num) / self.frame_rate
                    if time_elapsed <= 0:
                        continue

                    speed_meters_per_second = distance_covered / time_elapsed
                    speed_km_per_hour = speed_meters_per_second * 3.6

                    if obj not in total_distance:
                        total_distance[obj] = {}

                    if track_id not in total_distance[obj]:
                        total_distance[obj][track_id] = 0

                    total_distance[obj][track_id] += distance_covered

                    for frame_num_batch in range(frame_num, last_frame):
                        if track_id not in tracks[obj][frame_num_batch]:
                            continue
                        tracks[obj][frame_num_batch][track_id]['speed'] = speed_km_per_hour
                        tracks[obj][frame_num_batch][track_id]['distance'] = total_distance[obj][track_id]
