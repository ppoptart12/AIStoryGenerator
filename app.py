from flask import Flask, render_template, jsonify
from story_generator import StoryGenerator

app = Flask(__name__)

# Create an instance of MyClass
_story_generator = StoryGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_function', methods=['POST'])
def run_function():
    # This will call the do_something method of my_object
    _story_generator._get_plot_points()
    generated_story, plot_points = _story_generator.retrieve_AI_story()
    return jsonify(main_result=generated_story, additional_info=plot_points)

if __name__ == '__main__':
    app.run(debug=True)
