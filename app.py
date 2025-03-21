from flask import Flask, request, jsonify, render_template
from groq import Groq
import os
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the Groq client using the API key from .env
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    try:
        # Call the Groq API for response
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": user_input}],
            model="llama-3.3-70b-versatile",
            stream=False
        )
        bot_response = response.choices[0].message.content
        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)