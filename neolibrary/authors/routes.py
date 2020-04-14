from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask import current_app as app
from flask_login import current_user, login_required
from neolibrary import graph, book_covers
from neolibrary.main.utils import sidebar
from neolibrary.models import Author 
from neolibrary.authors.forms import AuthorForm

authors = Blueprint('authors', __name__)

@authors.route("/author/<int:author_id>")
def author(author_id):
    author = Author().match(graph).where("id(_)=%d"%author_id).first()
    if author:
        return render_template('author.html', title="Details",author=author, author_id=author_id, image_folder=book_covers, sidebar=sidebar())
    return render_template('no_such_item.html', item="Author")



@authors.route("/author/<int:author_id>/update", methods=['GET', 'POST'])
@login_required
def update_author(author_id):
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
                               form=form, legend='Update Author', sidebar=sidebar())
    elif not author:
        return render_template('no_such_item.html', item="Author", sidebar=sidebar())



@authors.route("/author/<int:author_id>/delete", methods=['POST'])
@login_required
def delete_author(author_id):
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

    return render_template('list_authors.html', authors=authors, sidebar=sidebar())
    
