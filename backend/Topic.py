from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tree import Tree


class Topic:
    def __init__(self, id: int, text: str):
        self.id: int = id
        self.text = text

    def add_parent(self, parent: Tree):
        self.parent = parent
