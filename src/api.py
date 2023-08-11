import os
from flask import Flask, request, jsonify, send_from_directory
from civicllama import chatbot
from logger import logger
from flask_cors import CORS
from civicllama import reset as reset_chatbot
from civicllama import load_documents

app = Flask(__name__)
cors = CORS(app, resources={r"/ask": {"origins": ["https://civicgpt.beltway.cloud"]}})


@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend', filename)


@app.route('/ask', methods=['POST'])
def ask():
    try:
        question = request.json.get('question')
        if question:
            logger.info(f"Received question: {question}")
            response = chatbot(question)
            logger.info(f"Sending response: {response}")
            return jsonify({'response': response})

        logger.error("No question provided")  # Log error
        return jsonify({'error': 'No question provided'}), 400

    except Exception as e:
        logger.critical(f"An error occurred: {e}")  # Log any critical error
        return jsonify({'error': 'A server error occurred'}), 500


@app.route('/reset', methods=['POST'])
def reset():
    reset_chatbot()
    logger.warning("Chatbot reset")
    return jsonify({'status': 'ok'})


if __name__ == "__main__":
    app.run(port=3090, host='0.0.0.0', debug=False)

app.logger.addHandler(logger)
