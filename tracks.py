"""
Includes functions for finding tracks.
"""
from __future__ import annotations
import csv

from dataclasses import dataclass
from datatypes import Track, Tree, Queue
from typing import Any, Optional

class TrackList:
    """
    Python object used to interact with a given dataset containing Spotify Music

    All methods use a track id as the first input, and return a Track Object or a List of Track Objects

    Overview:

    .get_track(track_id) : Return Track object associated with ID
    .find_similar(track_id) : Return Track object that is closes to the Track associated with ID
    .find_multiple_similar(track_id, count) Return list of size 'count' of Track objects close
                                            close to the Track associated with ID


    """

    _tracks: dict[str, Track]
    _algorithm: _Brute_Force

    def __init__(self, dataset: str) -> None:
        """
        Loads data into Track Objects
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

        self._algorithm = _Brute_Force(track_points)

    def get_track(self, track_id: str) -> Track:
        """
        Return Track associated with track_id, if Track does not exist return None

        Using dictionary lookup, consider switching to binary search
        """
        if track_id in self._tracks:
            return self._tracks[track_id]
        else:
            return None
        
    def get_similarity(self, track_id1: str, track_id2: str) -> float:
        if track_id1 in self._tracks and track_id2 in self._tracks:
            point1 = self._algorithm.get_point(track_id1)
            point2 = self._algorithm.get_point(track_id2)
        else:
            raise NameError
        
        return point1.euclidiean_distance(point2)
        

        
    def find_similar(self, track_id: str) -> Track:
        """
        Return Track closest to Track associated with track_id
        """
        point = self._algorithm.get_point(track_id)

        similar_id = self._algorithm.find_similar(point)
        print(similar_id)

        return self.get_track(similar_id)
    
    def find_multiple_similar(self, track_id: str, count: int) -> list[Track]:
        point = self._algorithm.get_point(track_id)

        similar_ids = self._algorithm.find_multiple_similar(point, count)

        return [self.get_track(id) for id in similar_ids]

    
    def add_track(self, Track):
        raise NotImplementedError

class _KdTree:
    """
    [depreciated]

    KDTree used to search for similar tracks
    """
    root: _Point
    left: Tree
    right: Tree
    parent: Optional[_KdTree]

    def __init__(self):
        self.root = None
        self.left = None
        self.right = None
        self.parent = None
            
    def _sort_points(self, axis: int, points: list[_Point]) -> list[_Point]:
        """Return sorted list along the specified axis"""
        return sorted(points, key = lambda item: item.vector[axis])
    
    def _split_median(self, axis: int, points: list[_Point]) -> tuple[_Point, float]:
        """Return tuple containing median _KdTreePoint, median along axis, the left and right lists
        If points is even length, the median is the lower of the two middle points.
        
        pre-conditions:
         - points must be sorted in increasing order
        """

        n = len(points)

        if n % 2 == 1:
            mid = n // 2
        else:
            mid = n // 2 - 1

        median = points[mid]
        
        return (median, median.vector[axis], points[:mid], points[mid + 1:])

    def create_tree(self, points: list[_Point], current_axis: int, parent: Optional[_KdTree] = None):
        # todo: try redoing this in the __init__ function (?)

        if points == []:
            self.parent = parent
        else:
            points = self._sort_points(current_axis, points)

            median_point, median_value, left_points, right_points = self._split_median(current_axis, points)

            self.root = median_point
            self.parent = parent

            self.left, self.right = _KdTree(), _KdTree()

            if right_points != []:
                self.right.create_tree(right_points, (current_axis + 1) % len(points[0].vector), self)

            if left_points != []:
                self.left.create_tree(left_points, (current_axis + 1) % len(points[0].vector), self)

       

    
    def find_similar(self, point: _Point, number: int) -> list[str]:
        # todo: fix this man this sucks

        points_so_far = Queue()

    def _recursive_find_similar(self, vector: tuple[float], current_axis: int):
        # todo: this asw this also sucks bad
        if self.left._root is None and self.right._root is None:
            return self.root
        elif vector[current_axis] > 0: # temp number
            pass

    def is_empty(self) -> bool:
        return self.root is None

    def __str__(self) -> str:
        return self._str_indented(0).rstrip()
    
    def _str_indented(self, rank: int) -> str:

        if self.is_empty():
            return ""
        else:
            return (rank * " " + f"{self.root}\n"
                    + self.right._str_indented(rank + 1)
                    + self.left._str_indented(rank + 1))
        
class _Brute_Force:
    """
    This object is to brute force to find similar tracks
    """

    points: list[_Point]

    def __init__(self, points:dict[str, tuple[float]]):
        id_so_far = []
        points_formatted = []

        for x in points:
            if x not in id_so_far:
                points_formatted.append(_Point(points[x], x))

        self.points = points_formatted

    def get_point(self, id) -> _Point:
        """Return _Point associated with ID"""

        for p in self.points:
            if id == p.name:
                return p
        
        return None

    def find_similar(self, point: _Point) -> str:
        """ Return str associated with the point closest to input point


        notice: uses brute force, time complexity O(n) where n is len(self.points)
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
    point_a = _Point((2, 3, 2, 8, 4, 4, 7, 6), "a")
    point_b = _Point((9, 0, 5, 0, 3, 8, 7, 9), "b")
    test_points_1 = [_Point((2, 3, 2, 8, 4, 4, 7, 6), "a"),
                   _Point((9, 0, 5, 0, 3, 8, 7, 9), "b"),
                   _Point((3, 0, 4, 3, 2, 0, 8, 1), "c"),
                   _Point((6, 0, 1, 5, 8, 9, 1, 2), "d"),
                   _Point((5, 9, 8, 2, 8, 7, 4, 9), "e"),
                   _Point((7, 6, 1, 5, 8, 5, 9, 1), "f"),]
    
    test_points_2 = [_Point((2, 3, 2, 8, 4, 4, 7, 6), "a"),
                   _Point((9, 0, 5, 0, 3, 8, 7, 9), "b"),
                   _Point((3, 0, 4, 3, 2, 0, 8, 1), "c")]
    
    test_points_3 = [_Point((1, 0, 0), "x"),
                     _Point((0, 1, 0), "y"),
                     _Point((0, 0, 1), "z")]
    



    tk = TrackList("dataset.csv")

    bruh = tk._algorithm.get_point("29RiulWABWHcTRLkDqVCl1")

    bruh2 = tk.find_multiple_similar("29RiulWABWHcTRLkDqVCl1", 15)

    print("29RiulWABWHcTRLkDqVCl1" == "29RiulWABWHcTRLkDqVCl1")

    for i in range(len(bruh2)):
        print(i, " : ", bruh2[i].track_name, ":", (bruh.euclidiean_distance(tk._algorithm.get_point(bruh2[i].track_id))))

    print(bruh.euclidiean_distance(tk._algorithm.get_point(bruh2[-1].track_id)))

    print("bruh 2.5")

    print(tk.get_track("5waHhqlk8iTweFuHeZz9CZ"))

    # print(test_tree._sort_points(0, test_points_2))
    # print("-" * 60)
    # print(test_tree._sort_points(1, test_points_2))
    # print("-" * 60)
    # print(test_tree._sort_points(2, test_points_2))