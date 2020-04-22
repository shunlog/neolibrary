from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask import current_app as app
from flask_login import current_user, login_required
from neolibrary import graph, book_covers
from neolibrary.models import Tag
from neolibrary.tags.forms import TagForm

tags = Blueprint('tags', __name__)

@tags.route("/tag/<int:tag_id>")
def tag(tag_id):
    tag = Tag().match(graph).where("id(_)=%d"%tag_id).first()
    if tag:
        return render_template('tag.html', title="Details",tag=tag, tag_id=tag_id, book_covers=book_covers)
    return render_template('no_such_item.html', item="Tag")



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
