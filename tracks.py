"""
Contains one Object, the TrackList object
TrackList is used to interact with a dataset.
"""
from __future__ import annotations
import csv

from datatypes import Track


class TrackList:
    """
    Python object used to interact with a given dataset containing Spotify Music

    All methods use a track id as the first input, and return a Track Object or a List of Track Objects

    Overview:

    self.get_track(track_id) : Return Track object associated with ID
    self.find_similar(track_id) : Return Track object that is closes to the Track associated with ID
    self.find_multiple_similar(track_id, count) Return list of size 'count' of Track objects close
                                            close to the Track associated with ID


    attributes:
     - _tracks : maps id to Track objects (Track objects hold metadata about the song such as artist, track name and album)
     - _algorithm : Search algorithm used to find similar tracks to input ID
    """

    _tracks: dict[str, Track]
    _algorithm: _KDTree

    def __init__(self, dataset: str) -> None:
        """
        Load track data from a CSV file and initialize the search algorithm.

        Preconditions:
            - dataset must be a valid path to a CSV file.
            - The CSV file must have a header row followed by data rows.
            - Expected CSV columns (by index) include:
                8: danceability,
                9: energy,
                11: loudness,
                13: speechiness,
                14: acousticness,
                15: instrumentalness,
                16: livevness,
                17: valence
        """

        self._tracks = {}

        # Contains points used in kd tree for search algorithm, in the form {name: (points)}
        track_points = {}

        with open(dataset, "r", encoding="UTF-8") as data:
            track_reader = csv.reader(data)

            next(track_reader)

            for track in track_reader:

                track_point = (
                    float(track[8]), # danceability
                    float(track[9]), # energy
                    float(track[11]), # loudness
                    float(track[13]), # speechiness
                    float(track[14]), # acousticness
                    float(track[15]), # instrumentalness
                    float(track[16]), # livevness
                    float(track[17]) # valence
                    )

                track_points[track[1]] = track_point

                #Left out key, mode, tempo and time signature as currently we do not need it.
                new_track = Track(
                    track_id = track[1],
                    artists = track[2],
                    album_name = track[3],
                    track_name = track[4],
                    popularity = track[5],
                    duration_ms = track[6],
                    explicit = track[7],
                    track_genre = track[20],
                    )

                self._tracks[track[1]] = new_track

        self._algorithm = _KDTree(track_points)

    def get_track(self, track_id: str) -> Track:
        """
        Retrieve the Track object associated with the given track_id if found. Else, return None.
        """
        if track_id in self._tracks:
            return self._tracks[track_id]
        else:
            return None

    def get_similarity(self, track_id1: str, track_id2: str) -> float:
        raise NotImplementedError

    def find_similar(self, track_id: str) -> Track:
        """
        Find and return the Track object most similar to the track associated with track_id.

        Preconditions:
            - track_id must exist in the dataset.
        """
        point = self._algorithm.get_point(track_id)

        similar_id = self._algorithm.nearest_neighbour(point)

        return self.get_track(similar_id)

    def find_multiple_similar(self, track_id: str, count: int) -> list[Track]:
        """
        Find and return a list of Track objects that are most similar to the track associated with track_id.

        Preconditions:
            - track_id must exist in the dataset.
            - count must be a positive integer.
        """
        point = self._algorithm.get_point(track_id)

        similar_ids = self._algorithm.n_nearest_neighbours(point, count)

        return [self.get_track(id) for id in similar_ids]

    def add_track(self, Track):
        raise NotImplementedError


class KDNode:
    """ One Node in a KD-Tree

    attributes:
     - point : tuple holding values of a song as vector points
     - label : id of the song references
     - left : KDNode to the 'left' compared with a specific dimension
     - right : KDNode to the 'right' compared with a specific dimension
    """
    def __init__(self, point:tuple[float], label:str=None, left:KDNode=None, right:KDNode=None):
        """
        Initialize a KDNode with the given point, label, and optional child nodes.
        """
        self.point = point
        self.label = label
        self.left = left
        self.right = right

class _KDTree:
    """ KD-Tree implementation to attempt to search for similar points

    attributes:
     - data : Dictionary mapping id to vector points
     - root : First node of the Tree
    """
    def __init__(self, data):
        """
        Initialize the KD-Tree with the provided data.

        Preconditions:
            - data must be a dictionary mapping track IDs (str) to non-empty tuples of floats.
        """
        self.data = data
        points = [(key, value) for key, value in data.items()]
        self.root = self._build_tree(points, depth=0)

    def get_point(self, id) -> tuple[float]:
        """
        Retrieve the feature vector associated with the given track ID.

        Preconditions:
            - id must be a non-empty string.
        """
        if id in self.data:
            return self.data[id]
        else:
            return None

    def _build_tree(self, points, depth):
        """
        Recursively build the KD-Tree from the list of (track_id, feature_vector) tuples.

        Preconditions:
            - points must be a list of tuples where each tuple contains a track ID (str) and a feature vector (tuple of floats).
            - depth must be a non-negative integer.
        """
        if not points:
            return None

        k = len(points[0][1])  # Dimension of data
        axis = depth % k

        points.sort(key=lambda x: x[1][axis])
        median = len(points) // 2

        return KDNode(
            point=points[median][1],
            label=points[median][0],
            left=self._build_tree(points[:median], depth + 1),
            right=self._build_tree(points[median + 1:], depth + 1)
        )

    def nearest_neighbour(self, target) -> str:
        """
        Find and return the track ID of the point in the KD-Tree closest to the target vector.

        Preconditions:
            - target must be a non-empty tuple of floats with the same dimension as the feature vectors.
        """
        def _nn(node, depth, best):
            if node is None:
                return best

            k = len(target)
            axis = depth % k

            next_best = best
            dist_sq = sum((node.point[i] - target[i]) ** 2 for i in range(k))
            if best is None or dist_sq < best[1]:
                next_best = (node.label, dist_sq)

            next_branch = node.left if target[axis] < node.point[axis] else node.right
            alt_branch = node.right if target[axis] < node.point[axis] else node.left

            next_best = _nn(next_branch, depth + 1, next_best)
            if abs(node.point[axis] - target[axis]) ** 2 < next_best[1]:
                next_best = _nn(alt_branch, depth + 1, next_best)

            return next_best

        return _nn(self.root, 0, None)[0]

    def n_nearest_neighbours(self, target: tuple[float], n: int) -> list[str]:
        """
        Find and return the track IDs of the n closest points to the target vector.

        Preconditions:
            - target must be a non-empty tuple of floats with the same dimension as the feature vectors.
            - n must be a positive integer.
        """
        neighbors = []

        def _search(node, depth):
            if node is None:
                return

            k = len(target)
            axis = depth % k

            dist_sq = sum((node.point[i] - target[i]) ** 2 for i in range(k))

            if len(neighbors) < n:
                neighbors.append((node.label, dist_sq))
                neighbors.sort(key=lambda x: x[1])
            elif dist_sq < neighbors[-1][1]:
                neighbors[-1] = (node.label, dist_sq)
                neighbors.sort(key=lambda x: x[1])

            next_branch = node.left if target[axis] < node.point[axis] else node.right
            alt_branch = node.right if target[axis] < node.point[axis] else node.left

            _search(next_branch, depth + 1)
            if abs(node.point[axis] - target[axis]) ** 2 < neighbors[-1][1]:
                _search(alt_branch, depth + 1)

        _search(self.root, 0)
        return [label for label, x in neighbors]


class _Brute_Force:
    """
    [Depreciated]
    Not in use anymore, but we keep it for testing/fallback in case kdTree fails to work

    This object is to brute force to find similar tracks
    """

    points: list[_Point]

    def __init__(self, points:dict[str, tuple[float]]):
        """
        Initialize the brute force search algorithm.

        Preconditions:
            - points must be a dictionary mapping track IDs (str) to non-empty tuples of floats.
        """
        id_so_far = []
        points_formatted = []

        for x in points:
            if x not in id_so_far:
                points_formatted.append(_Point(points[x], x))

        self.points = points_formatted

    def get_point(self, id) -> _Point:
        """
        Retrieve the _Point object associated with the given track ID.

        Preconditions:
            - id must be a non-empty string.
        """

        for p in self.points:
            if id == p.name:
                return p

        return None

    def find_similar(self, point: _Point) -> str:
        """
        Find and return the track ID of the _Point closest to the given point.

        Note: Uses brute force with O(n) time complexity, where n is len(self.points).

        Preconditions:
            - point must be an instance of _Point.
            - point.vector must have the same dimension as other points.
        """
        current_distance = 9999
        current_id = ""

        p = self.points[0]

        for p in self.points:

            distance = point.euclidiean_distance(p)
            if distance < current_distance and p.name != point.name:
                current_distance = distance
                current_id = p.name

        return current_id

    def find_multiple_similar(self, point: _Point, count:int) -> list[str]:
        """
        Find and return a list of track IDs for the count closest points to the given point.

        Preconditions:
            - point must be an instance of _Point.
            - count must be a positive integer.
        """
        distance_dict = {p.name: point.euclidiean_distance(p) for p in self.points}
        distance_dict.pop(point.name)

        sorted_list = sorted(distance_dict, key = lambda k:distance_dict[k])

        return sorted_list[:count]


class _Point:
    """Helper object to represent one vector point, used in _KdTree"""
    vector: tuple[float]
    name: str

    def __init__(self, vector: tuple[float], name: str):
        self.vector = vector
        self.name = name

    def __str__(self) -> str:
        return f"{self.name}: " + str(self.vector)

    def euclidiean_distance(self, comparison: _Point) -> float:
        """
        Return distance from self to the comparison point.

        Pre-conditions:
            - len(self.vector) == len(comparison.vector)
            - len(self.vector) > 0
        """

        v1 = self.vector
        v2 = comparison.vector

        sum_so_far = 0.0

        for i in range(len(v1)):
            sum_so_far += (v1[i]-v2[i]) ** 2

        return sum_so_far ** 0.5

if __name__ == "__main__":
    tk = TrackList("dataset.csv")

    my_list = tk.find_multiple_similar("29RiulWABWHcTRLkDqVCl1", 15)

    for i in range(len(my_list)):
        print(i, " : ", my_list[i].track_name)
