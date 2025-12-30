from flask import Flask, render_template, send_from_directory, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app with custom folders for templates and static files
app = Flask(__name__, 
            template_folder='codr-web',  # Folder containing HTML templates
            static_folder='css')         # Folder containing CSS files

# Configure secret key for session management and flash messages
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'local-test-key-123')

# Gmail configuration for sending emails
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True  # Use TLS for security
app.config['MAIL_USERNAME'] = os.getenv('GMAIL_USER')      # Email from environment
app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_PASSWORD')  # Password from environment
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('GMAIL_USER')

# Initialize Flask-Mail extension
mail = Mail(app)

# SIMPLE Email validation function
def is_valid_email(email):
    """
    Basic email validation function
    Checks for:
    - Presence of @ symbol
    - Domain has at least one dot
    - Domain extension has at least 2 characters
    """
    # Check if @ symbol exists
    if '@' not in email:
        return False
    
    # Split email into local part and domain
    local_part, domain = email.split('@', 1)
    
    # Check if domain has at least one dot
    if '.' not in domain:
        return False
    
    # Check if domain extension has at least 2 characters (like .com, .org)
    if len(domain.split('.')[-1]) < 2:
        return False
        
    return True

# Route for homepage
@app.route("/")
def index():
    """Render the main homepage"""
    return render_template("index.html")

# Contact page route - handles both GET and POST requests
@app.route("/Contact", methods=['GET', 'POST'])  
def contact():
    """Handle contact form submissions and display contact page"""
    if request.method == 'POST':
        # Get form data and strip whitespace
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message_content = request.form.get('message', '').strip()
        
        # Basic validation - check all fields are filled
        if not name or not email or not message_content:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('contact'))
        
        # Email validation using custom function
        if not is_valid_email(email):
            flash('Please enter a valid email address (example: name@gmail.com).', 'error')
            return redirect(url_for('contact'))        
        
        try:
            # Create email message
            msg = Message(
                subject=f'New Contact Form Message from {name}',
                recipients=['yash.khandelwal.codr@gmail.com'],  # Recipient email
                body=f"""
Name: {name}
Email: {email}
Message: {message_content}

Sent from your website contact form.
                """
            )
            # Send the email
            mail.send(msg)
            flash('Thank you! Your message has been sent successfully.', 'success')
        except Exception as e:
            # Handle email sending errors
            print(f"Error sending email: {e}")
            flash('Sorry, there was an error sending your message. Please try again.', 'error')
        
        # Redirect back to contact page after form submission
        return redirect(url_for('contact'))
    
    # For GET requests, simply render the contact page
    return render_template("contact.html")

# Route for lessons page
@app.route("/Lessons")
def lessons():
    """Render the lessons page"""
    return render_template("lessons.html")

# Route for perspective page
@app.route("/Perspective")
def perspective():
    """Render the perspective page"""
    return render_template("perspective.html")

# Route for projects page
@app.route("/Projects & Builds")
def projects():
    """Render the projects and builds page"""
    return render_template("projects.html")

# DYNAMIC ROUTES LAST (catch-all for blog posts)
@app.route('/<post_name>')
def serve_blog_post(post_name):
    """
    Dynamic route to serve blog posts from different folders
    Searches through multiple post directories to find the requested post
    """
    folders = [
        'codr-web/post/lessons-post',    # Lessons posts folder
        'codr-web/post/project-post',    # Project posts folder
        'codr-web/post/perspective-post' # Perspective posts folder
    ]
    
    # Search through each folder for the requested post
    for folder in folders:
        try:
            # Try to serve the post from current folder
            return send_from_directory(folder, f"{post_name}.html")
        except:
            # If not found, continue searching other folders
            continue
    
    # If post not found in any folder, return 404 error
    return "Post not found", 404

# Route to serve static assets (images, etc.)
@app.route('/assets/<path:filename>')
def serve_images(filename):
    """Serve static assets from the assets directory"""
    return send_from_directory('assets', filename)

# Main entry point - run the Flask application
if __name__ == "__main__":
    app.run(debug=True, port=0)  # debug=True for development, port=0 for automatic port selection