from __future__ import annotations
from typing import List 
from flask import jsonify
import uuid

class Question():
  def __init__(self, text: str):
    self.id: int = uuid.uuid1().int
    self.text: str = text
    self.votes: int = 1

class Tree():
  def __init__(self, question: Question, level: int):
    self.question: Question = question
    self.children: List[Tree] = []
    self.level: int = level

  def add_node(self, node: Tree):
    self.children.append(node)

  def add_node_list(self, node_list: List[Tree]):
    for node in node_list: 
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
  def __init__(self, head, children):
    self.head = self.text_to_tree(head, 0)
    children_list = [self.text_to_tree(child, 1) for child in children]
    self.head.add_node_list(children_list)
    self.all_nodes = [self.head] + children_list

  def text_to_tree(self, text: str, level: int) -> Tree:
    return Tree(Question(text), level)

  def network_to_JSON_format(self):
    return self.head.to_JSON_format()

  def get_potential_link(self, text): 
    
    def search_for_link(node):

      if node.level
      if find_keyword_match(text, )

    return search_for_link(self.head)
  