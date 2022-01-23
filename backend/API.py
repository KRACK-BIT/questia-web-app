from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS
from QuestionNetwork import QuestionNetwork

# configuration
DEBUG = True


head = "Forces"
children = ["Definitions", "Newton's Forces", "Other"]
question_network = QuestionNetwork(head, children)

"""
print(question_network.network_to_JSON_format())
print("\n" * 4)
question_network.pprint()
print("\n" * 4)

print("\n" * 4)
question_network.add_question("What are forces", question_network.head.children[1].value.id)
question_network.pprint()
print("\n" * 5)

print(question_network.network_to_JSON_format())
"""

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

bp = Blueprint("api", __name__)

# get questions tree
@bp.route("/get-tree", methods=["GET"])
def get_tree():
    return jsonify(question_network.network_to_JSON_format())


@bp.route("/get-potential-link", methods=["POST"])
def get_potential_link():
    json = request.get_json()
    id = question_network.get_potential_link(json["text"])
    return jsonify({"id": id})


@bp.route("/confirm-link", methods=["PUT"])
def confirm_link():
    json = request.get_json()
    question_network.add_question(json["text"], json["link"])
    return "success"


@bp.route("/vote-for-question", methods=["PUT"])
def vote_for_question():
    json = request.get_json()
    question_network.upvote_question(json["question_id"])


app.register_blueprint(bp, url_prefix="/api")

if __name__ == "__main__":
    app.run()
