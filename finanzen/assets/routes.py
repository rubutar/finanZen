from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, jsonify)
from flask_login import current_user, login_required
import yfinance as yf
from finanzen import db
from finanzen.models import Asset
from finanzen.assets.forms import AssetForm

assets = Blueprint('assets', __name__)

@assets.route("/calc")
@login_required
def calc():
    assets = Asset.query.all()
    # Calculate total investment, return, and percentage return
    total_investment = sum([inv.total_price for inv in assets])
    # For simplicity, let's assume current price is fixed, in real cases, fetch from API
    current_price = 100  # Placeholder value, replace with actual logic
    total_return = sum([(current_price * inv.quantity) - inv.total_price for inv in assets])
    percentage_return = (total_return / total_investment) * 100 if total_investment > 0 else 0

    return render_template('calc_index.html', assets=assets, total_investment=total_investment, total_return=total_return, percentage_return=percentage_return)



@assets.route("/calc/new", methods=['GET', 'POST'])
@login_required
def new_calc():
    form = AssetForm()
    if form.validate_on_submit():
        asset = Asset(ticker=form.ticker.data, price=form.price.data, owner=current_user)
        db.session.add(asset)
        db.session.commit()
        flash('Your asset has been added!', 'success')
        return redirect(url_for('assets.calc'))
    return render_template('calc_new.html', title='New Asset', 
                           form=form, legend='New Asset') 


@assets.route('/search_ticker', methods=['GET'])
def search_ticker():
    query = request.args.get('query', '')
    if query:
        tickers = yf.Ticker(query).info
        return jsonify(tickers)
    return jsonify([])

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


