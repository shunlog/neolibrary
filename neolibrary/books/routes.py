import os
import secrets
from json import dumps
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask import current_app as app
from flask_login import current_user, login_required
from neolibrary import graph, book_covers
from neolibrary.books.forms import BookForm
from neolibrary.models import Book, Author, Tag
from neolibrary.books.utils import match_book, data_to_obj_ls, save_book_cover, download_book_cover, delete_book_cover

books = Blueprint('books', __name__)

@books.route("/book/new", methods=['GET', 'POST'])
@login_required
def new_book():
    if not current_user.is_admin:
        flash(f'Admin account required!', 'danger')
        return redirect(url_for('main.home'))

    form = BookForm()
    if form.validate_on_submit():

        picture_file = None
        if form.picture.data:
            picture_file = save_book_cover(form.picture.data)
        elif form.link.data:
            picture_file = download_book_cover(form.link.data)
            if not picture_file:
                form.link.errors.append("Error requesting file")
                return render_template('create_book.html', title='New Book',
                                       form=form, legend='New Book', book_covers=book_covers)

        book = match_book("create (b:Book) return b", 'b')
        if not book:
            flash('The book couldn\'t be created!', 'danger')
            return redirect(url_for('books.new_book'))
        print(book)
        if picture_file:
            book.image_file = picture_file

        # creating book by query or else py2neo will match existing one
        # if the title is same
        book.title=form.title.data.strip()

        authors_ls=form.hidden_authors.data
        for a_name in authors_ls.split(','):
            a_name = a_name.strip()
            author = Author().match(graph, a_name).first()
            if (not author) and (a_name != ''):
                author = Author()
                author.name = a_name
                graph.push(author)
                book.authors.add(author)
            elif a_name != '':
                book.authors.add(author)
        tags_ls=form.hidden_tags.data
        for t_name in tags_ls.split(','):
            t_name = t_name.strip()
            tag = Tag().match(graph, t_name).first()
            if (not tag) and (t_name != ''):
                tag = Tag()
                tag.name = t_name
                graph.push(tag)
                book.tags.add(tag)
            elif t_name != '':
                book.tags.add(tag)

        print(book.__node__)
        graph.push(book)
        flash('Your book has been created!', 'success')
        return redirect(url_for('books.new_book'))
    return render_template('create_book.html', title='New Book',
                           form=form, legend='New Book', book_covers=book_covers)


@books.route("/book/<int:book_id>")
def book(book_id):
    book = Book().match(graph).where("id(_)=%d"%book_id).first()
    if not book:
        return render_template('no_such_item.html', item="Book")
    return render_template('book.html', title="Details",book=book, book_id=book_id, book_covers=book_covers)


@books.route("/book/<int:book_id>/update", methods=['GET', 'POST'])
@login_required
def update_book(book_id):
    if not current_user.is_admin:
        flash(f'Admin account required!', 'danger')
        return redirect(url_for('main.home'))

    book = Book().match(graph).where("id(_)=%d"%book_id).first()
    form = BookForm()

    if book and form.validate_on_submit():
        # picture
        if form.picture.data:
            delete_book_cover(book.image_file)
            picture_file = save_book_cover(form.picture.data)
            book.image_file = picture_file

        # title
        book.title=form.title.data

        # delete previous authors
        authors_to_remove = []
        for a in book.authors:
            authors_to_remove.append(a)
        for a in authors_to_remove:
            book.authors.remove(a)

        # delete previous tags
        tags_to_remove = []
        for t in book.tags:
            tags_to_remove.append(t)
        for t in tags_to_remove:
            book.tags.remove(t)

        authors_ls=form.hidden_authors.data
        for a_name in authors_ls.split(','):
            a_name = a_name.strip()
            a_name = " ".join(a_name.split())
            author = Author().match(graph, a_name).first()
            if (not author) and (a_name != ''):
                author = Author()
                author.name = a_name
                graph.push(author)
                book.authors.add(author)
            elif a_name != '':
                book.authors.add(author)

        tags_ls=form.hidden_tags.data
        for t_name in tags_ls.split(','):
            t_name = t_name.strip()
            t_name = " ".join(t_name.split())
            tag = Tag().match(graph, t_name).first()
            if (not tag) and (t_name != ''):
                tag = Tag()
                tag.name = t_name
                graph.push(tag)
                book.tags.add(tag)
            elif t_name != '':
                book.tags.add(tag)

        graph.push(book)
        flash('The book has been updated!', 'success')
        return redirect(url_for('books.book', book_id=book_id))

    elif book and request.method == 'GET':
        form.title.data = book.title

        prefilled={}
        authors_ls = []
        for a in book.authors:
            authors_ls.append(a.name)
        prefilled['authors'] = ','.join(authors_ls)

        tags_ls = []
        for t in book.tags:
            tags_ls.append(t.name)
        prefilled['tags'] = ','.join(tags_ls)

        prefilled = dumps(prefilled)
        print(prefilled)

        return render_template('create_book.html', title='Update Book',
                               form=form, legend='Update Book', prefilled=prefilled)
    elif not book:
        return render_template('no_such_item.html', item=book)

@books.route("/book/<int:book_id>/delete", methods=['POST'])
@login_required
def delete_book(book_id):
    if not current_user.is_admin:
        flash(f'Admin account required!', 'danger')
        return redirect(url_for('main.home'))
    book = Book().match(graph).where("id(_)=%d"%book_id).first()
    delete_book_cover(book.image_file)
    graph.delete(book)
    flash('The book has been deleted!', 'success')
    return redirect(url_for('main.home'))


@books.route("/book/<int:book_id>/review/<string:action>", methods=['POST'])
@login_required
def review_book(book_id, action):
    book = Book().match(graph).where("id(_)=%d"%book_id).first()
    if action == "add_like":
        if book in current_user.books_disliked:
            current_user.books_disliked.remove(book)
        current_user.books_liked.add(book)
    elif action == "rm_like":
        current_user.books_liked.remove(book)
    elif action == "add_dislike":
        if book in current_user.books_liked:
            current_user.books_liked.remove(book)
        current_user.books_disliked.add(book)
    elif action == "rm_dislike":
        current_user.books_disliked.remove(book)
    else:
        flash("Something wrong", 'danger')
        return redirect(url_for('books.book', book_id=book_id))
    graph.push(current_user)
    return redirect(url_for('books.book', book_id=book_id))

@books.route("/list_books", methods=['GET','POST'])
def list_books():
    if not current_user.is_admin:
        flash(f'Admin account required!', 'danger')
        return redirect(url_for('main.home'))
    books = Book().match(graph)
    if request.method == 'POST':
            book_ls = request.form.getlist('book')
            print(book_ls)
            count = 0
            for b_id in book_ls:
                count += 1
                b_obj = Book().match(graph).where("id(_) = %d" % int(b_id)).first()
                if b_obj.image_file and b_obj.image_file != "default.png":
                    if not delete_book_cover(b_obj.image_file):
                        flash('Book cover couldn\'t be deleted!', 'danger')
                        return redirect(url_for('books.list_books'))
                print("Deleted node ",b_obj.__node__)
                graph.delete(b_obj)
            flash(str(count)+' books have been deleted!', 'success')
            return redirect(url_for('books.list_books'))

    return render_template('list_books.html', books=books)
