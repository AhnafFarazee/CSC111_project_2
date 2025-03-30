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
    Holds information about tracks

    attributes:
    
    representation invariants:

    """
    track_id: str
    artists: list[str]
    album_name: str
    track_name: str
    popularity: int
    duration_ms: int
    explicit: bool
    track_genre: str

class Tree:
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        return self._root is None
    
    def __len__(self) -> int:
        if self.is_empty():
            return 0
        else:
            size = 1
            for subtree in self._subtrees:
                size += subtree.__len__()
            return size
    
    def __contains__(self, item: Any) -> bool:
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True
            return False
        
    def remove(self, item:Any) -> bool:

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
        if self._subtrees == []:
            self._root = None
        else:
            last_subtree = self._subtrees.pop()
            self._root = last_subtree._root
            self._subtrees.extend(last_subtree._subtrees)

    def add_subtrees(self, subtrees: list[Tree]) -> None:
        self._subtrees.extend(subtrees)

class Queue:
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
        if self.is_empty():
            pass
        else:
            return self._items.pop(0)
        
    def items(self) -> list:
        return self._items.copy()

if __name__ == "__main__":
    print("ok")


class Graph:
    """Graph object"""
    verticies: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initializes an empty graph"""
        self._verticies = {}

    def add_item(self, item: Any) -> None:
        if item not in self._verticies:
            self._verticies[item] = _Vertex(item)
    
    def add_edge(self, item_1:_Vertex, item_2:_Vertex) -> None:
        if item_1 in self._verticies and item_2 in self._verticies:
            self._verticies[item_1].neighbours.add(self._verticies[item_2])
            self._verticies[item_2].neighbours.add(self._verticies[item_1])
        else:
            raise NameError


class _Vertex:
    """Vertex object"""
    item: str
    neighbours: set[_Vertex]

    def __init__(self, item: Optional[Any], neighbours: Optional[set[_Vertex]]) -> None:
        self.item = item
        self.neighbours = neighbours