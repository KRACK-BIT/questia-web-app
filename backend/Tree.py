from __future__ import annotations
from typing import List
from Topic import Topic 
from Question import Question 

class Tree():
  def __init__(self, value: Question | Topic, level: int) -> None:

    if (type(value) is Question):
      self.type = "Question" 
    else:
      self.type = "Topic"

    self.value: Question | Topic = value
    self.children: List[Tree] = []
    self.level: int = level

  def add_child(self, node: Tree) -> None:
    self.children.append(node)

  def add_child_list(self, node_list: List[Tree]) -> None:
    for node in node_list: 
      self.children.append(node)

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

