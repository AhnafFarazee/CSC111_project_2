"""
Includes functions for finding tracks.
"""
from __future__ import annotations
import csv

from dataclasses import dataclass
from datatypes import Track, Tree, Queue
from typing import Any, Optional

class TrackList:

    _tracks: dict[str, Track]

    def __init__(self, dataset: str) -> None:
        """
        Loads data into Track Objects
        """

        self._tracks = {}

        # Contains points used in kd tree for search algorithm, in the form ((data), track_id) where (data)
        # is a n dimensional vector
        track_points = []

        with open(dataset, "r", encoding="UTF-8") as data:
            track_reader = csv.reader(data)
            for track in track_reader:

                track_point = ((
                    track[8], # danceability
                    track[9], # energy
                    track[11], # loudness
                    track[13], # speechiness
                    track[14], # acousticness
                    track[15], # instrumentalness
                    track[16], # livevness
                    track[17] # valence
                ), track[1])

                track_points.append(track_point)
                
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

    def get_track(self, track_id: str) -> Track:
        """
        Return Track associated with track_id, if Track does not exist return None

        Using dictionary lookup, consider switching to binary search
        """
        if track_id in self._tracks:
            return self._tracks[track_id]
        else:
            return None
    
    def add_track(self, Track):
        pass #todo finish this

class _KdTree:
    """
    Creates a k-d tree to search close neighbours ygm

    information:
    - 
    attributes:
    - _root contains tuple holding vector data and track_id
    """
    root: str
    left: Tree
    right: Tree
    parent: Optional[_KdTree]

    def __init__(self):
        self.root = None
        self.left = None
        self.right = None
        self.parent = None
            
    def _sort_points(self, axis: int, points: list[_KdTreePoint]) -> list[_KdTreePoint]:
        """Return sorted list along the specified axis"""
        return sorted(points, key = lambda item: item.vector[axis])
    
    def _find_median(self, axis: int, points: list[_KdTreePoint]) -> tuple[_KdTreePoint, float]:
        """Return tuple containing median _KdTreePoint and the median along axis
        If points is even length, the median is the lower of the two middle points.
        
        pre-conditions:
         - points must be sorted in increasing order
        """

        n = len(points)

        if n == 1:
            median = points[0]
            return (median, median.vector[axis])
        elif n % 2 != 0:
            median = points[int((n + 1) // 2)]
            return (median, median.vector[axis])
        else:
            median = points[int(n // 2) - 1]
            return (median, median.vector[axis])

    def create_tree(self, points: list[_KdTreePoint], current_axis: int, parent: Optional[_KdTree] = None):
        if points == []:
            self.root = None
            self.left = None
            self.right = None
            self.parent = parent
        else:
            points = self._sort_points(current_axis, points)
            current_axis = (current_axis + 1) % 8 # cycles axis in order

            median_point, median_value = self._find_median(current_axis, points)

            self.root = median_point
            self.parent = parent
            self.right = _KdTree()
            self.left = _KdTree()

            right_points = [x for x in points if x.vector[current_axis] > median_value]
            self.right.create_tree(right_points, current_axis, self)
            
            left_points = [x for x in points if x.vector[current_axis] < median_value]
            self.left.create_tree(left_points, current_axis, self)
    
    def find_reccomendations(self, point: _KdTreePoint, number: int) -> list[Track]:
        # todo: fix this man this sucks

        points_so_far = Queue()

    def _recursive_find_reccomendations(self, order, track_profile, number, tracks_so_far):
        # todo: this asw this also sucks bad
        if self.left is None and self.right is None:
            pass


@dataclass
class _KdTreePoint:
    """Helper object to represent one vector point, used in _KdTree"""
    vector: tuple[float]
    name: str




if __name__ == "__main__":

    print(int((3+1) / 2))
    test_points = [_KdTreePoint((2, 3, 2, 8, 4, 4, 7, 6), "a"),
                   _KdTreePoint((9, 0, 5, 0, 3, 8, 7, 9), "b"),
                   _KdTreePoint((3, 0, 4, 3, 2, 0, 8, 1), "c"),
                   _KdTreePoint((6, 0, 1, 5, 8, 9, 1, 2), "d"),
                   _KdTreePoint((5, 9, 8, 2, 8, 7, 4, 9), "e"),
                   _KdTreePoint((7, 6, 1, 5, 8, 5, 9, 1), "f"),]
    
    test_tree = _KdTree()
    sorted_points = test_tree._sort_points(2, test_points)
    for point in sorted_points:
        print(point)
    print(test_tree._find_median(2, sorted_points))

    test_tree.create_tree(test_points, 0)