from . import db

from flask import Blueprint, \
                  render_template, \
                  url_for, \
                  request, \
                  redirect

from .models import Article

blog = Blueprint('blog', __name__)


"""
query - обращение к бд. order_by - сортировка при выводе.
first - первый элемент из списка. all - все эл-ты списка
"""


@blog.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@blog.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


@blog.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Error while deleting the article"


@blog.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        author = request.form['author']

        article = Article(title=title,
                          intro=intro,
                          text=text,
                          author=author)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "You have a miss while creating article"
    else:
        return render_template('create-article.html')


@blog.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "You have a miss while updating article"
    else:
        return render_template('update-article.html', article=article)
