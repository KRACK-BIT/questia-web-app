from __future__ import annotations
from typing import List 
from flask import jsonify
import uuid

class Question():
  def __init__(self, text: str):
    self.id : int = uuid.uuid1().int
    self.text : str = text
    self.votes: int = 1

class Tree():
  def __init__(self, question: Question):
    self.question: Question = question
    self.children: List[Tree] = []

  def add_node(self, node: Tree):
    self.children.append(node)

  def to_JSON_format(self):
    question = self.question
    children = self.children
    return { 
             "id" : question.id, 
             "text" : question.text,
             "size" : question.votes, 
             "children" : [child.to_JSON_format() for child in children]
           }

class QuestionNetwork(): 
  def __init__(self):
    """
    Manually set base 
    """
    self.head = Tree(Question("Forces"))
    self.head.add_node(Tree(Question("Definitions")))
    self.head.add_node(Tree(Question("Newton's Forces")))
    self.head.add_node(Tree(Question("Other")))

  def network_to_JSON_format(self):
    return self.head.to_JSON_format()

  