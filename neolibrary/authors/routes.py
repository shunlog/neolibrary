from math import ceil
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask import current_app as app
from flask_login import current_user, login_required
from neolibrary import graph, book_covers, book_covers_path, Config
from neolibrary.models import Author, Book
from neolibrary.authors.forms import AuthorForm
from neolibrary.books.utils import iter_pages, validate_page_number

authors = Blueprint('authors', __name__)

@authors.route("/author/<int:author_id>", methods=['GET'])
def author(author_id):
    author = Author().match(graph).where("id(_)=%d" % author_id).first()
    if not author:
        return render_template('no_such_item.html', item="Author")
    global book_covers_path
    if not book_covers_path:
        book_covers_path = url_for('static', filename=book_covers)
    page = request.args.get('page', 1, type=int)
    lim = Config.BOOKS_LIMIT

    query = "match (b:Book)<--(a:Author) where id(a)=$author_id \
    return count(b)"
    dt = graph.run(query, author_id=author_id)
    count = dt.evaluate()

    pages = ceil(count/lim)
    page = validate_page_number(page, pages)
    page_ls = iter_pages(pages, page)

    query_books = "match (b:Book)<--(a:Author) where id(a)=$author_id \
    return b skip $skip limit $limit"
    dt = graph.run(query_books,  author_id=author_id,
                   limit=lim, skip=(page-1)*lim)
    books = [Book.wrap(node[0]) for node in dt]

    return render_template('author.html', title="Details", author=author,
                           author_id=author_id, page_ls=page_ls,
                           current_page=page, books=books,
                           book_covers_path=book_covers_path)



@authors.route("/author/<int:author_id>/update", methods=['GET', 'POST'])
@login_required
def update_author(author_id):
    if not current_user.is_admin:
        flash(f'Admin account required!', 'danger')
        return redirect(url_for('main.home'))
    author = Author().match(graph).where("id(_)=%d"%author_id).first()
    form = AuthorForm()
    if author and form.validate_on_submit():
        author.name = form.name.data
        graph.push(author)
        flash('The author has been updated!', 'success')
        return redirect(url_for('authors.author', author_id=author_id))
    elif author and request.method == 'GET':
        form.name.data = author.name
        return render_template('update_author.html', title='Update Author',
                               form=form, legend='Update Author')
    elif not author:
        return render_template('no_such_item.html', item="Author")



@authors.route("/author/<int:author_id>/delete", methods=['POST'])
@login_required
def delete_author(author_id):
    if not current_user.is_admin:
        flash(f'Admin account required!', 'danger')
        return redirect(url_for('main.home'))
    author = Author().match(graph).where("id(_)=%d"%author_id).first()
    graph.delete(author)
    flash('The author has been deleted!', 'success')
    return redirect(url_for('main.home'))


@authors.route("/author/<int:author_id>/like", methods=['POST'])
@login_required
def like_author(author_id):
    author = Author().match(graph).where("id(_)=%d"%author_id).first()
    graph.delete(author)
    flash('The author has been deleted!', 'success')
    return redirect(url_for('main.home'))


@authors.route("/list_authors", methods=['GET','POST'])
def list_authors():
    if not current_user.is_admin:
        flash(f'Admin account required!', 'danger')
        return redirect(url_for('main.home'))
    authors = Author().match(graph)
    if request.method == 'POST':
        author_ls = request.form.getlist('author')
        count = 0
        for a_name in author_ls:
            count += 1
            a_obj = Author().match(graph, a_name).first()
            graph.delete(a_obj)
            print("Deleted node ",a_obj.__node__)
            flash(str(count)+' authors have been deleted!', 'success')
        return redirect(url_for('authors.list_authors'))

    return render_template('list_authors.html', authors=authors)
