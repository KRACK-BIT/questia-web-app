from KeywordMatch import KeywordMatch
from Tree import Tree
from Topic import Topic 
from Question import Question 
class QuestionNetwork(): 
  def __init__(self, head, children):
    self.keyword_matcher = KeywordMatch()
    self.head = self.text_to_topic_tree_object(head, 0)
    self.head.add_child_list([self.text_to_topic_tree_object(child, 1) for child in children])
    self.all_questions = {child.value.id : child.value for child in self.head.children}

  def text_to_topic_tree_object(self, text: str, level: int) -> Tree:
    topic = Topic(text)
    tree = Tree(topic, level)
    topic.add_parent(tree)
    return tree 

  def text_to_question_tree_object(self, text: str, level: int) -> Tree:
    topic = Question(text)
    tree = Tree(topic, level)
    topic.add_parent(tree)
    return tree

  def network_to_JSON_format(self):

    def recursive_search(node, connections): 
      for child in node.children: 
        connections.append({"source":node.value.id, "target":child.value.id})

    connections = []
    recursive_search(self.head, connections)

    return {
      "links" : connections,
      "nodes" : [node.parent.to_JSON_format() for node in self.all_questions.values()] 
    }

  def get_potential_link(self, text): 
    
    def search_for_link(node):
      if not node:
        return False

      value = node.value
      if node.type == "Question" and self.keyword_matcher.find_keyword_match(text, value.text): 
        return value.id
      else:
        for child in node.children:
          search_result = search_for_link(child)
          if search_result:
            return search_result
        return False 

    return search_for_link(self.head)
  
  def upvote_question(self, question_id):
    self.all_questions[question_id] += 1

  def add_question(self, text, link_id): 
    link_val = self.all_questions[link_id]
    link_node = link_val.parent
    link_node.add_child(self.text_to_question_tree_object(text, link_node.level + 1))

  def pprint(self):
    def pprint_recurse(node):
      node.pprint()
      for child in node.children: 
        pprint_recurse(child)

    pprint_recurse(self.head)