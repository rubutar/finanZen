from flask import render_template, request, Blueprint, send_file
from finanzen.models import Post

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    return render_template("about.html", title='About')

@main.route('/pdf')
def serve_pdf():
    # Path to the PDF file
    path_to_pdf = 'templates/Portfolio.pdf'
    return send_file(path_to_pdf)

