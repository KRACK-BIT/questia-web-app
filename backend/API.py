from flask import Flask, jsonify
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
CORS(app, resources={r'/*': {'origins': '*'}})

# get questions tree
@app.route('/get-tree', methods=['GET'])
def get_tree():
  return jsonify(question_network.network_to_JSON_format()) 

@app.route('/get-potential-link', methods=['POST'])
def get_potential_link(request):
  json = request.get_json()
  question_network.get_potential_link(json["text"])

@app.route('/confirm-link', methods=['PUT'])
def confirm_link(request):
  json = request.get_json() 
  question_network.add_question(json["text"], json["link"])

@app.route('/vote-for-question', methods=['PUT'])
def vote_for_question(request): 
  json = request.get_json()
  question_network.upvote_question(json["question_id"])

if __name__ == '__main__':
    app.run()