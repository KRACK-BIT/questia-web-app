from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tree import Tree


class Question:
    def __init__(self, id: int, text: str):
        self.id: int = id
        self.text: str = text
        self.votes: int = 1

    def add_parent(self, parent: Tree):
        self.parent = parent
