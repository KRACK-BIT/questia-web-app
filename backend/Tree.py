from __future__ import annotations

from typing import List

from Question import Question
from Topic import Topic


class Tree:
    def __init__(self, value: Question | Topic, level: int, parent) -> None:
        self.value: Question | Topic = value
        self.children: List[Tree] = []
        self.level: int = level
        self.parent = parent

    def add_child(self, node: Tree) -> None:
        self.children.append(node)

    def add_child_list(self, node_list: List[Tree]) -> None:
        for node in node_list:
            self.children.append(node)

    def to_JSON_format(self):
        value = self.value
        if isinstance(value, Topic):
            return {"id": value.id, "type": "Topic", "text": value.text}
        else:
            return {
                "id": value.id,
                "type": "Question",
                "text": value.text,
                "size": value.votes,
            }

    """
  def to_JSON_format(self): # -> Dict[id, text, size, children : Dict[...]]
    value = self.value
    children = self.children
    if self.type == "Topic":
      return {
        "type" : "Topic",
        "id" : value.id,
        "text" : value.text,
        "children" : [child.to_JSON_format() for child in children]
      }
    else:
      return {
        "type" : "Question",
        "id" : value.id,
        "text" : value.text,
        "size" : value.votes,
        "children" : [child.to_JSON_format() for child in children]
      }
  """

    def pprint(self):
        if isinstance(self.value, Topic):
            print(
                "  " * self.level
                + f"Type: {type(self.value)} Text: {self.value.text} Level: {self.level}"
            )
        else:
            print(
                "  " * self.level
                + f"Type: {type(self.value)} Text: {self.value.text} Level: {self.level} Votes: {self.value.votes}"
            )
