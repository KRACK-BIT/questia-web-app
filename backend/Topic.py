import uuid

class Topic(): 
  def __init__(self, text: str):
    self.id: int = uuid.uuid1().int 
    self.text = text

  def add_parent(self, parent: Tree):
    self.parent = parent 