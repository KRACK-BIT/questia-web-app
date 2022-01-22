from flask import Flask, jsonify
from flask_cors import CORS
import QuestionNetwork

# configuration
DEBUG = True

head = "Forces"
children = ["Definitions", "Newton's Forces", "Other"]
question_network = QuestionNetwork.QuestionNetwork(head, children)
print(question_network.network_to_JSON_format())

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# get questions tree
@app.route('/get-tree', methods=['GET'])
def get_tree():
  return jsonify(question_network.network_to_JSON_format()) 

@app.route('/get-potential-link', method=['POST'])
def get_potential_link(text):
  question_network.get_potential_link(text)

@app.route('/confirm-link', method=['PUT'])
def confirm_link(text, link):
  question_network.add_question(text, link)


"""
# get questions tree
@app.route('/send-question', methods=['GET'])
def send_question():
    return jsonify('ping')

# get questions tree
@app.route('/send-upvote', methods=[''])
def send_upvote():
    return jsonify('ping')
"""

if __name__ == '__main__':
    app.run()