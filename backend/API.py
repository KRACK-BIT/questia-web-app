from flask import Flask, jsonify
from flask_cors import CORS
import QuestionNetwork

# configuration
DEBUG = True
question_network = QuestionNetwork.QuestionNetwork()
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