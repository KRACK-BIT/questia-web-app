from KeywordMatch import KeywordMatch
from Tree import Tree, Topic, Question
class QuestionNetwork(): 
  def __init__(self, head, children):
    self.keyword_matcher = KeywordMatch()
    self.head = self.text_to_topic(head, 0)
    self.head.add_child_list([self.text_to_topic(child, 1) for child in children])
    self.all_questions = {}

  def text_to_topic_tree_object(self, text: str, level: int) -> Tree:
    topic = Topic(text)
    tree = Tree(topic, level)
    topic.add_parent(tree)
    return tree 

  def text_to_question_tree_object(self, text: str, level: int) -> Tree:
    topic = Question(text), level
    tree = Tree(topic, level)
    topic.add_parent(tree)
    return tree

  def network_to_JSON_format(self):
    return self.head.to_JSON_format()

  def get_potential_link(self, text): 
    
    def search_for_link(node):
      question = node.question
      if node.type == "Question" and self.keyword_matcher.find_keyword_match(text, question.text): 
        return question.id
      else:
        for child in node.children:
          search_for_link(child)

    return search_for_link(self.head)
  
  def upvote_question(self, question_id):
    self.all_questions[question_id] += 1

  def add_question(self, text, link_id): 
    link_val = self.all_questions[link_id]
    link_node = link_val.parent
    link_node.add_child(self.text_to_question_tree_object(text, link_val.level + 1))