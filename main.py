from flask import Flask, render_template, send_from_directory

# Create an instance of the Flask class

app = Flask(__name__, 
            template_folder='codr-web',  # Your HTML folder
            static_folder='css')  

# Define a route for the homepage
@app.route('/assets/<path:filename>')
def serve_images(filename):
    return send_from_directory('assets', filename)

@app.route('/<post_name>')
def serve_lesson_post(post_name):
    return send_from_directory('codr-web/post/lessons-post', f"{post_name}.html")
@app.route('/<post_name>')

def serve_project_post(post_name):
    return send_from_directory('codr-web/posts/project-post', f"{post_name}.html")

@app.route('/<post_name>')
def serve_perspective_post(post_name):
    return send_from_directory('codr-web/posts/perspective-post', f"{post_name}.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Contact")
def contact():
    return render_template("contact.html")

@app.route("/Lessons")
def lessons():
    return render_template("lessons.html")

@app.route("/Perspective")
def perspective():
    return render_template("perspective.html")

@app.route("/Projects & Builds")
def projects():
    return render_template("projects.html")


# To run the application (in a development environment):
if __name__ == "__main__":
    app.run(debug=True, port=0) 