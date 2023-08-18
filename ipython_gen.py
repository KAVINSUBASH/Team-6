from flask import Flask, render_template, request
from nbformat import write, v4 as nbf
import json

# Global variable to store questions
questions = []
app = Flask(__name__)
# This function renders the index.html template
@app.route('/', methods=['GET', 'POST'])
def home():
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the JSON file uploaded by the user
        file = request.files.get('json_file')
        # Get the question and answer entered by the user
        question = request.form.get('question')
        answer = request.form.get('answer')

        # If the user has uploaded a JSON file, load the questions from the file
        if file:
            json_data = json.load(file)
            json_questions = json_data.get('questions')
            # If the file contains questions, add them to the global questions list
            if json_questions:
                questions.extend(json_questions)

        # If the user has entered a question and answer, add them to the global questions list
        if question and answer:
            questions.append({'question': question, 'answer': answer})

        # Generate the Jupyter notebook
        generate_notebook(questions)

    # Render the index.html template
    return render_template('index.html')

# This function generates the Jupyter notebook
def generate_notebook(questions):
    # Create a new Jupyter notebook object
    nb = nbf.new_notebook()
    # Create a list of cells
    cells = []

    # Iterate over the questions and create a markdown cell for each question
    for i, question in enumerate(questions, start=1):
        markdown_input = f"### Question {i}\n\n{question['question']}"
        cells.append(nbf.new_markdown_cell(source=markdown_input))

    # Iterate over the questions and create a code cell for each answer
    for i, question in enumerate(questions, start=1):
        code_input = f"print('Answer: {question['answer']}')"
        cells.append(nbf.new_code_cell(source=code_input))

    # Set the cells property of the notebook object
    nb['cells'] = cells

    # Open the questions.ipynb file in write mode
    with open('questions.ipynb', 'w') as f:
        # Write the notebook object to the file
        write(nb, f)

    # Print a message to indicate that the notebook file has been generated successfully
    print("Notebook file 'questions.ipynb' generated successfully.")

# This is the main function
if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
