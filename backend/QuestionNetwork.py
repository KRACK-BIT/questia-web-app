from KeywordMatch import KeywordMatch
from TreeDataStructures import Tree, Topic, Question
class QuestionNetwork(): 
  def __init__(self, head, children):
    self.keyword_matcher = KeywordMatch()
    self.head = self.text_to_topic(head, 0)
    self.head.add_node_list([self.text_to_topic(child, 1) for child in children])
    self.all_questions = {}

  def text_to_topic(self, text: str, level: int) -> Tree:
    return Tree(Topic(text), level)

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
