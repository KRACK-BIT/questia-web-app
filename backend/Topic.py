from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Tree import Tree
    
import uuid

class Topic(): 
  def __init__(self, text: str):
    self.id: int = uuid.uuid1().int 
    self.text = text

  def add_parent(self, parent: Tree):
    self.parent = parent 