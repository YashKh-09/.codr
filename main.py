from flask import Flask, render_template, send_from_directory, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, 
            template_folder='codr-web',
            static_folder='css')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'local-test-key-123')

# Gmail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('GMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('GMAIL_USER')

mail = Mail(app)

# SIMPLE Email validation function
def is_valid_email(email):
    # Simple check for @ and . in the domain part
    if '@' not in email:
        return False
    
    local_part, domain = email.split('@', 1)
    
    # Check if domain has at least one dot
    if '.' not in domain:
        return False
    
    # Check if there's text after the last dot
    if len(domain.split('.')[-1]) < 2:
        return False
        
    return True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Contact", methods=['GET', 'POST'])  
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message_content = request.form.get('message', '').strip()
        
        # Basic validation
        if not name or not email or not message_content:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('contact'))
        
        # Email validation
        if not is_valid_email(email):
            flash('Please enter a valid email address (example: name@gmail.com).', 'error')
            return redirect(url_for('contact'))        
        try:
            msg = Message(
                subject=f'New Contact Form Message from {name}',
                recipients=['yash.khandelwal.codr@gmail.com'],
                body=f"""
Name: {name}
Email: {email}
Message: {message_content}

Sent from your website contact form.
                """
            )
            mail.send(msg)
            flash('Thank you! Your message has been sent successfully.', 'success')
        except Exception as e:
            print(f"Error sending email: {e}")
            flash('Sorry, there was an error sending your message. Please try again.', 'error')
        
        # Use url_for to ensure consistent redirect
        return redirect(url_for('contact'))
    
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

# DYNAMIC ROUTES LAST (catch-all)
@app.route('/<post_name>')
def serve_blog_post(post_name):
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