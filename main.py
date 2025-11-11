from flask import Flask, render_template, send_from_directory

app = Flask(__name__, 
            template_folder='codr-web',
            static_folder='css')

# SPECIFIC ROUTES FIRST (most important!)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Contact")
def contact():
    return render_template("contact.html")

@app.route("/Lessons")  # Match your navigation exactly!
def lessons():
    return render_template("lessons.html")

@app.route("/Perspective")
def perspective():
    return render_template("perspective.html")

@app.route("/Projects & Builds")
def projects():
    return render_template("projects.html")

# DYNAMIC ROUTES LAST (catch-all)
@app.route('/<post_name>')
def serve_blog_post(post_name):
    # Try different post folders in order
    folders = [
        'codr-web/post/lessons-post',
        'codr-web/posts/project-post', 
        'codr-web/posts/perspective-post'
    ]
    for folder in folders:
        try:
            return send_from_directory(folder, f"{post_name}.html")
        except:
            continue

    return "Post not found", 404

@app.route('/assets/<path:filename>')
def serve_images(filename):
    return send_from_directory('assets', filename)
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)