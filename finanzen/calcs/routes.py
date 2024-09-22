from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from finanzen import db
from finanzen.models import Asset
from finanzen.calcs.forms import CalcForm

calcs = Blueprint('calcs', __name__)


@calcs.route("/calc")
@login_required
def calc():
    assets = Asset.query.order_by(Asset.purchase_date.desc())
    return render_template('calc_index.html', assets=assets)

@calcs.route("/calc/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = CalcForm()
    if form.validate_on_submit():
        asset = Asset(ticker=form.ticker.data, quantity=form.quantity.data, 
                    purchase_price=form.purchase_price.data, purchase_date=form.purchase_date.data, owner=current_user)
        db.session.add(asset)
        db.session.commit()
        flash('Your asset has been added!', 'success')
        return redirect(url_for('calcs.calc'))
    return render_template('calc_new.html', title='New Asset', 
                           form=form, legend='Update Asset') 

# Function to fetch ticker symbols (e.g., from S&P 500)
def get_tickers():
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA", "NFLX", "NVDA", "JPM", "V"]
    return tickers

@calcs.route('/record_asset', methods=['GET', 'POST'])
def record_asset():
    tickers = get_tickers()
    
    if request.method == 'POST':
        ticker = request.form['ticker']
        quantity = int(request.form['quantity'])
        purchase_price = float(request.form['purchase_price'])
        purchase_date = request.form['purchase_date']
        
        # Create a new asset instance
        new_asset = Asset(
            ticker=ticker, 
            quantity=quantity, 
            purchase_price=purchase_price, 
            purchase_date=purchase_date
        )
        
        # Add the asset to the database
        db.session.add(new_asset)
        db.session.commit()
        return redirect(url_for('calcs.calc'))
    return render_template('calc_new.html', title='New Asset', 
                           form=form, legend='New Asset') 


# @posts.route("/post/<int:post_id>")
# def post(post_id):
#     post = Post.query.get_or_404(post_id)
#     return render_template('post.html', title=post.title, post=post)

# @posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# @login_required
# def update_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('posts.post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html', title='Update Post', 
#                            form=form, legend='Update Post') 

# @posts.route("/post/<int:post_id>/delete", methods=['POST'])
# @login_required
# def delete_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     db.session.delete(post)
#     db.session.commit()
#     flash('Your post has been deleted!', 'success')
#     return redirect(url_for('main.home'))


