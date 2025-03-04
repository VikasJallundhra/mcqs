from flask import Flask, request, jsonify
import google.generativeai as genai
import json
import re  # To extract JSON safely
import os
import gunicorn

app = Flask(__name__)

# Configure API Key (Ensure it's activated for API usage)
genai.configure(api_key="AIzaSyBqq3ey1O2qGIB_9LTMGgjAlUoln7uESSo")

@app.route('/generate-mcqs', methods=['POST'])
def generate_mcqs():
    try:
        # Choose the correct model
        model = genai.GenerativeModel("gemini-1.5-pro-latest")

        # Get JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Missing JSON data"}), 400

        text = data.get("text", "Write about India and Indian people")  # Default text
        num_item = data.get("num_item", 5)  # Default to 5 questions
        difficulty = data.get("difficulty", "medium")  # Default difficulty

        # Define the prompt
        prompt = f"""
        Generate {num_item} multiple-choice questions (MCQs) based on the provided text.

        - If difficulty is 'easy', questions should be factual and straightforward.
        - If difficulty is 'medium', questions should require some inference.
        - If difficulty is 'hard', questions should require deep analysis and critical thinking.

        **Rules for questions and answers**:
        - No long phrases or sentences.
        - Questions and answers should be concise and clear.

        # If no text is provided, return the following JSON response:
        
        {{
          "status": "error",
          "message": "No input text provided. Please provide a text to generate MCQs."
        }}

        Provide the output in **valid JSON format ONLY** with this structure:

        {{
          "status": "success",
          "difficulty": "{difficulty}",
          "num_item": {num_item},
          "questions": [
            {{
              "question": "Sample question?",
              "options": ["Option A", "Option B", "Option C", "Option D"],
              "answer": "Correct answer"
            }}
          ]
        }}

        Text: {text}
        """

        # Generate response
        response = model.generate_content(prompt)

        # Ensure response exists
        if not hasattr(response, "text") or not response.text:
            return jsonify({"status": "error", "message": "Empty response from Gemini AI"}), 500

        # Extract JSON from response using regex (handles extra text)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if not match:
            return jsonify({"status": "error", "message": "Invalid JSON response from AI"}), 500

        mcqs_json = json.loads(match.group())

        return jsonify(mcqs_json)  # Return parsed JSON response

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get the port assigned by Render
    app.run(host='0.0.0.0', port=port)  # Bind to all available network interfaces

        
