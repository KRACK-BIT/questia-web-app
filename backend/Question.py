import uuid

class Question():
  def __init__(self, text: str):
    self.id: int = uuid.uuid1().int
    self.text: str = text
    self.votes: int = 1

  def add_parent(self, parent: Tree):
    self.parent = parent 