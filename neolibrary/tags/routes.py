from math import ceil
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask import current_app as app
from flask_login import current_user, login_required
from neolibrary import graph, book_covers, book_covers_path, Config
from neolibrary.models import Tag, Book
from neolibrary.tags.forms import TagForm
from neolibrary.books.utils import iter_pages, validate_page_number

tags = Blueprint('tags', __name__)

@tags.route("/tag/<int:tag_id>")
def tag(tag_id):
    tag = Tag().match(graph).where("id(_)=%d"%tag_id).first()
    if not tag:
        return render_template('no_such_item.html', item="Tag")
    global book_covers_path
    if not book_covers_path:
        book_covers_path = url_for('static', filename=book_covers)
    page = request.args.get('page', 1, type=int)
    lim = Config.BOOKS_LIMIT

    query = "match (b:Book)<--(a:Tag) where id(a)=$tag_id \
    return count(b)"
    dt = graph.run(query, tag_id=tag_id)
    count = dt.evaluate()

    pages = ceil(count/lim)
    page = validate_page_number(page, pages)
    page_ls = iter_pages(pages, page)

    query_books = "match (b:Book)<--(a:Tag) where id(a)=$tag_id \
    return b skip $skip limit $limit"
    dt = graph.run(query_books,  tag_id=tag_id,
                   limit=lim, skip=(page-1)*lim)
    books = [Book.wrap(node[0]) for node in dt]

    return render_template('tag.html', title="Details", tag=tag,
                           tag_id=tag_id, page_ls=page_ls,
                           current_page=page, books=books,
                           book_covers_path=book_covers_path)



@tags.route("/tag/<int:tag_id>/update", methods=['GET', 'POST'])
@login_required
def update_tag(tag_id):
    if not current_user.is_admin:
        flash(f'Admin account required!', 'danger')
        return redirect(url_for('main.home'))
    tag = Tag().match(graph).where("id(_)=%d"%tag_id).first()
    form = TagForm()
    if tag and form.validate_on_submit():
        tag.name = form.name.data
        graph.push(tag)
        flash('The tag has been updated!', 'success')
        return redirect(url_for('tags.tag', tag_id=tag_id))
    elif tag and request.method == 'GET':
        form.name.data = tag.name
        return render_template('update_tag.html', title='Update Tag',
                               form=form, legend='Update Tag')
    elif not tag:
        return render_template('no_such_item.html', item="Tag")



@tags.route("/tag/<int:tag_id>/delete", methods=['POST'])
@login_required
def delete_tag(tag_id):
    if not current_user.is_admin:
        flash(f'Admin account required!', 'danger')
        return redirect(url_for('main.home'))
    tag = Tag().match(graph).where("id(_)=%d"%tag_id).first()
    graph.delete(tag)
    flash('The tag has been deleted!', 'success')
    return redirect(url_for('main.home'))


@tags.route("/list_tags", methods=['GET','POST'])
def list_tags():
    if not current_user.is_admin:
        flash(f'Admin account required!', 'danger')
        return redirect(url_for('main.home'))
    tags = Tag().match(graph)
    if request.method == 'POST':
        tag_ls = request.form.getlist('tag')
        count = 0
        for a_name in tag_ls:
            count += 1
            a_obj = Tag().match(graph, a_name).first()
            graph.delete(a_obj)
            print("Deleted node ",a_obj.__node__)
        flash(str(count)+' tags have been deleted!', 'success')
        return redirect(url_for('tags.list_tags'))

    return render_template('list_tags.html', tags=tags)


@tags.route("/add_tags", methods=['GET','POST'])
def add_tags():
    if not current_user.is_admin:
        flash(f'Admin account required!', 'danger')
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        books_ls = request.form.getlist('book')

    return render_template('add_tags.html')
