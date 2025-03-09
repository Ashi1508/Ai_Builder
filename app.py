from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API with your API key
genai.configure(api_key="AIzaSyC10gnIogn1voJf0TqVInQzfKnYJdON76A")

# Use the correct model name
model = genai.GenerativeModel('gemini-1.5-pro-latest')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    topic = data.get('topic')
    difficulty = data.get('difficulty')
    num_questions = data.get('numQuestions')

    # Validate input
    if not topic or not difficulty or not num_questions:
        return jsonify({"error": "Missing required fields: topic, difficulty, or numQuestions"}), 400

    try:
        num_questions = int(num_questions)
        if num_questions <= 0:
            return jsonify({"error": "Number of questions must be greater than 0"}), 400
    except ValueError:
        return jsonify({"error": "Invalid number of questions"}), 400

    # Generate MCQs using Gemini API
    questions = []
    prompt = f"""
    Generate {num_questions} multiple-choice questions about {topic} with {difficulty} difficulty.
    Format:
    <question>
    <option1>
    <option2>
    <option3>
    <option4>
    Correct Answer: <correct option letter>
    
    """

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        mcqs = response_text.split("\n\n")  # Split questions

        for mcq in mcqs:
            try:
                lines = mcq.split("\n")
                question_text = lines[0].replace("Question: ", "").strip()
                options = [line.strip() for line in lines[1:5]]
                correct_answer = lines[5].replace("Correct Answer: ", "").strip()

                questions.append({
                    "question": question_text,
                    "options": options,
                    "correct_answer": correct_answer,
                })
            except Exception as e:
                print(f"Error parsing MCQ: {e}")
                continue

    except Exception as e:
        print(f"Error generating question: {e}")
        return jsonify({"error": "Failed to generate questions. Please try again."}), 500

    if not questions:
        return jsonify({"error": "No questions generated. Please try again."}), 500

    return jsonify({"questions": questions})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)