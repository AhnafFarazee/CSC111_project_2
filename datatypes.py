"""
Contains common data types used in multiple files:
 - Track
 - Album
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Track:
    """
    Represents a musical track with associated metadata.

    Attributes:
        track_id: A unique identifier for the track.
        artists: The artist or artists performing the track.
        album_name: The album to which the track belongs.
        track_name: The title of the track.
        popularity: A measure of the track's popularity.
        duration_ms: The duration of the track in milliseconds.
        explicit: Indicates whether the track contains explicit content.
        track_genre: The genre of the track.

    Preconditions:
        - 0 <= popularity <= 100.
        - duration_ms >= 0.
    """
    track_id: str
    artists: str
    album_name: str
    track_name: str
    popularity: int
    duration_ms: int
    explicit: bool
    track_genre: str


class Tree:
    """
    A tree data structure where each node stores a value and a list of subtrees.

    Attributes:
        _root: The value stored at the current node. A value of None indicates an empty tree.
        _subtrees: The list of child trees.

    Representation Invariants:
        - Not (_root is None) or (_subtrees must be an empty list).
    """
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """
        Initialize a Tree with a root value and a list of subtrees.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """
        Check whether the tree is empty.
        """
        return self._root is None

    def __len__(self) -> int:
        """
        Compute the total number of nodes in the tree.
        """

        if self.is_empty():
            return 0
        else:
            size = 1
            for subtree in self._subtrees:
                size += subtree.__len__()
            return size

    def __contains__(self, item: Any) -> bool:
        """
        Check whether an item exists in the tree.
        """
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True
            return False

    def remove(self, item: Any) -> bool:
        """
        Remove the first occurrence of an item from the tree using a depth-first approach.

        If the item is found in the current node or any subtree, it is removed.
        """
        if self.is_empty():
            return False
        elif self._root == item:
            self._delete_root()
            return True
        else:
            for subtree in self._subtrees:
                deleted = subtree.remove(item)

                if deleted and subtree.is_empty():
                    self._subtrees.remove(subtree)
                    return True
                elif deleted:
                    return True

    def _delete_root(self) -> None:
        """
        Delete the root node of the tree.

        If subtrees are present, the root is replaced with the root of the last subtree,
        and that subtree's children are appended to the current tree's subtrees.
        If there are no subtrees, the tree becomes empty.
        """
        if self._subtrees == []:
            self._root = None
        else:
            last_subtree = self._subtrees.pop()
            self._root = last_subtree._root
            self._subtrees.extend(last_subtree._subtrees)

    def add_subtrees(self, subtrees: list[Tree]) -> None:
        """
       Add multiple subtrees to the current tree.
       """
        self._subtrees.extend(subtrees)


class Queue:
    """
    A simple First-In-First-Out (FIFO) queue implementation.

    Attributes:
        _items: The list storing the queue's elements.
    """
    _items: list

    def __init__(self) -> None:
        """Initialize a new empty Queue"""
        self._items = []

    def __len__(self) -> int:
        """Return length of Queue"""
        return len(self._items)

    def is_empty(self) -> bool:
        """Return whether this queue contains no items"""
        return self._items == []

    def enqueue(self, item: Any) -> None:
        """Add item to the back of this queue"""
        self._items.append(item)

    def enqueue_list(self, items: list) -> None:
        """Add multiple items to the back of this queue"""
        for item in items:
            self._items.append(item)

    def dequeue(self) -> Any:
        """
        Remove and return the item from the front of the queue.

        Preconditions:
            - The queue must not be empty when this method is called.
        """
        if self.is_empty():
            pass
        else:
            return self._items.pop(0)

    def items(self) -> list:
        """
        Return a shallow copy of the queue's items.
        """
        return self._items.copy()


class Graph:
    """
    Represents an undirected graph using an adjacency list structure.

    Attributes:
        _verticies: A mapping from each vertex's item to its corresponding _Vertex object.

    Representation Invariants:
        - All keys in _verticies must be hashable.
        - Each value in _verticies is a _Vertex whose 'item' attribute matches the key.
    """
    verticies: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initializes an empty graph"""
        self._verticies = {}

    def add_item(self, item: Any) -> None:
        """
        Add a new vertex with the specified item to the graph.

        Preconditions:
            - `item` must be hashable.
            - The item should not already exist in the graph.
        """
        if item not in self._verticies:
            self._verticies[item] = _Vertex(item)

    def add_edge(self, item_1:_Vertex, item_2:_Vertex) -> None:
        """
        Add an undirected edge between two vertices in the graph.

        Preconditions:
            - Both `item_1` and `item_2` must already exist in the graph.
            - The provided vertices should correspond to keys in _verticies.
        """
        if item_1 in self._verticies and item_2 in self._verticies:
            self._verticies[item_1].neighbours.add(self._verticies[item_2])
            self._verticies[item_2].neighbours.add(self._verticies[item_1])
        else:
            raise NameError


class _Vertex:
    """
    Represents a vertex in a graph. This is an internal class used by the Graph.

    Attributes:
        item: The value stored in the vertex.
        neighbours: A set of adjacent vertices.
    """
    item: str
    neighbours: set[_Vertex]

    def __init__(self, item: Optional[Any], neighbours: Optional[set[_Vertex]]) -> None:
        self.item = item
        self.neighbours = neighbours
