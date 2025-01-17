from KeywordMatch import KeywordMatch
from Question import Question
from Topic import Topic
from Tree import Tree


class QuestionNetwork:
    def __init__(self, head, children):
        self.current_id = 0
        self.keyword_matcher = KeywordMatch()
        self.head = self.text_to_topic_tree_object(head, 0, False)
        self.head.add_child_list(
            [self.text_to_topic_tree_object(child, 1, True) for child in children]
        )
        self.all_questions = {
            child.value.id: child.value for child in self.head.children
        }
        self.all_questions[self.head.value.id] = self.head.value

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
                recursive_search(child, connections)

        connections = []
        recursive_search(self.head, connections)

        return {
            "links": connections,
            "nodes": [
                node.parent.to_JSON_format() for node in self.all_questions.values()
            ],
        }

    def get_potential_link(self, text):
        highest_score = max(
            (
                (node, score)
                for (node, score) in (
                    (node, self.keyword_matcher.find_keyword_match(text, node.text))
                    for node in self.all_questions.values()
                )
                if score is not None
            ),
            key=lambda pair: pair[1],
            default=None,
        )

        if highest_score is None:
            return -1

        return highest_score[0].id

    def upvote_question(self, question_id):
        question = self.all_questions[question_id]
        if isinstance(question, Question):
            question.votes += 1
        else:
            raise TypeError(
                f"Only Questions can be upvoted, not nodes of type {type(question_id)} - see {question_id=}"
            )

    def add_question(self, text, link_id):
        link_node = self.all_questions[link_id].parent
        x = self.text_to_question_tree_object(text, link_node.level + 1, link_node)
        link_node.add_child(x)
        self.all_questions[x.value.id] = x.value

    def pprint(self):
        def pprint_recurse(node):
            node.pprint()
            for child in node.children:
                pprint_recurse(child)

        pprint_recurse(self.head)
