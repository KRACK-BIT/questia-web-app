from KeywordMatch import KeywordMatch
from Tree import Tree
from Topic import Topic
from Question import Question


class QuestionNetwork:
    def __init__(self, head, children):
        self.current_id = 5
        self.keyword_matcher = KeywordMatch()
        self.head = self.text_to_topic_tree_object(head, 0, False)
        self.head.add_child_list(
            [self.text_to_topic_tree_object(child, 1, True) for child in children]
        )
        self.all_questions = {
            child.value.id: child.value for child in self.head.children
        }
        self.all_questions[self.head.value.id] = self.head

    def text_to_topic_tree_object(self, text: str, level: int, is_head) -> Tree:
        topic = Topic(self.current_id, text)
        self.current_id += 1
        tree = Tree(topic, level, self.head if is_head else None)
        topic.add_parent(tree)
        return tree

    def text_to_question_tree_object(self, text: str, level: int, parent) -> Tree:
        topic = Question(self.current_id, text)
        self.current_id += 1
        tree = Tree(topic, level, parent)
        topic.add_parent(tree)
        return tree

    def network_to_JSON_format(self):
        def recursive_search(node, connections):
            for child in node.children:
                connections.append({"source": node.value.id, "target": child.value.id})

        connections = []
        recursive_search(self.head, connections)

        return {
            "links": connections,
            "nodes": [
                *[
                    node.parent.to_JSON_format()
                    for node in self.all_questions.values()
                    if node.parent
                ],
                self.head.to_JSON_format(),
            ],
        }

    def get_potential_link(self, text):
        def search_for_link(node):
            if not node:
                return False

            value = node.value
            if self.keyword_matcher.find_keyword_match(text, value.text):
                return value.id
            else:
                for child in node.children:
                    search_result = search_for_link(child)
                    if search_result:
                        return search_result
                return False

        x = search_for_link(self.head)
        if x:
            return x
        else:
            return self.head.value.id

    def upvote_question(self, question_id):
        self.all_questions[question_id] += 1

    def add_question(self, text, link_id):
        link_val = self.all_questions[link_id]
        link_node = link_val.value
        x = self.text_to_question_tree_object(text, link_val.level + 1, link_val)
        link_val.add_child(x)
        self.all_questions[x.value.id] = x.value

    def pprint(self):
        def pprint_recurse(node):
            node.pprint()
            for child in node.children:
                pprint_recurse(child)

        pprint_recurse(self.head)
