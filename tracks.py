"""
Includes functions for finding tracks.
"""

import csv

from datatypes import Track, Tree, Queue
from typing import Any, Optional

class TrackList:

    _tracks: dict[str, Track]

    def __init__(self, dataset: str) -> None:
        """
        Loads data into Track Objects
        """

        self._tracks = {}

        track_points = {}

        with open(dataset, "r", encoding="UTF-8") as data:
            track_reader = csv.reader(data)
            for track in track_reader:
                track_profile = {
                        "danceability": track[8],
                        "energy": track[9],
                        "loudness": track[11],
                        "speechiness": track[13],
                        "acousticness": track[14],
                        "instrumentalness": track[15],
                        "liveness": track[16],
                        "valence": track[17]
                    }
                
                track_points[track[1]] = track_profile


                new_track = Track(
                    track_id = track[1],
                    artists = track[2],
                    album_name = track[3],
                    track_name = track[4],
                    popularity = track[5],
                    duration_ms = track[6],
                    explicit = track[7],
                    track_profile = track_profile,
                    key = track[10],
                    mode = track[12],
                    tempo = track[18],
                    time_signature = track[19],
                    track_genre = track[20],
                    )

                self._tracks[track[1]] = new_track

    def get_track(self, track_id: str) -> Track:
        """
        Return Track associated with track_id, if Track does not exist return None
        """
        if track_id in self._tracks:
            return self._tracks[track_id]
        else:
            return None
    
    def add_track(self, Track):
        pass #todo finish this

class kd_tree:
    """
    Creates a k-d tree to search close neighbours ygm
    """
    _root: str
    _left: Tree
    _right: Tree
    _parent: Optional[Tree]

    def __init__(self,order:list[str], points: dict[str, dict[str, int]]):
        if points == {}:
            self._root = None
            self._left = None
            self._right = None
        else:
            sorted = self._sort_dictionary_by_key(order[0], points)
            order = order[1::] + order[0]
    
            tracks = [(track_id,track_profile[order[0]]) for track_id,track_profile in sorted.items]

            if len(tracks) % 2 == 1:
                median_track = tracks[len(tracks) // 2][0]
            else:
                median_track = tracks[len(tracks) // 2 -1][0]

            self._root = (median_track, points[median_track])

            self._right = kd_tree(order = order, points = {p: points[p] for p in points if points[p][order[0]] > points[median_track][order[0]]})
            self._right._parent = self
            self._left = kd_tree(order = order, points = {p: points[p] for p in points if points[p][order[0]] < points[median_track][order[0]]})
            self._left._parent = self
            
        
    def _sort_dictionary_by_key(self, axis: Any, dictionary: dict[str, dict[str, int]]):
        """Sorts a nested dictionary by the specified key"""

        return dict(sorted(dictionary.items(), key = lambda item: item[1][axis]))
    
    def _add_parent(self, parent: Tree) -> None:
        self._parent = parent
    
    def find_reccomendations(self, track: Track, number: int) -> list[Track]:
        # todo: fix this man this sucks

        track_profile = track.track_profile
        tracks_so_far = Queue()
        order = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence"]




    def _recursive_find_reccomendations(self, order, track_profile, number, tracks_so_far):
        # todo: this asw this also sucks bad
        if track_profile[order[0]] > self._root[1][order[0]]:
            order = order[1::] + order[0]
            self._right._recursive_find_reccomendations(order, track_profile, number, tracks_so_far)
        elif track_profile[order[0]] < self._root[1][order[0]]:
            order = order[1::] + order[0]
            self._left._recursive_find_reccomendations(order, track_profile, number, tracks_so_far)



if __name__ == "__main__":
    order = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence"]

    print("-" * 60)
    tracklist = TrackList("dataset.csv")