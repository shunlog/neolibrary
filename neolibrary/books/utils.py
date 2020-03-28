import os
import secrets
import urllib.request
from flask import current_app
from PIL import Image
from neolibrary import app, graph, book_covers
from neolibrary import book_covers
from neolibrary.models import Book 


def match_node(query, node):
    try:
        dt = graph.run(query).data()
        node = dt[0][node]
        book = Book().wrap(node)
        return book
    except:
        print("Error running query!")

def match_list_of_nodes(query, name):
    ls = []
    try:
        dt = graph.run(query).data()
        for node in dt:
            n = node[name]
            book = Book().wrap(n)
            ls.append(book)
        return ls
    except:
        print("Error running query!")


def save_book_cover(new_pic):
    global book_covers
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(new_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, book_covers, picture_fn)

    image = Image.open(new_pic)
    w, h = image.size
    wr = 2
    hr = 3
    ratio = wr/hr

    if w > h*ratio:
        print("width larger")
        left = (w - h*(wr/hr))/2
        top = 0
        print("Cropping",left,"from left")
        crop = image.crop((left, top, w-left, h-top))
    else:
        print("height larger")
        top = (h - w*(hr/wr))/2
        left = 0
        print("Cropping",top,"from top")
        crop = image.crop((left, top, w-left, h-top))

    crop.thumbnail([1000, 1500])
    crop.save(picture_path)
    return picture_fn

def download_book_cover(url):
    global book_covers
    f_ext = "."+url.split(".")[-1]
    print("Extension: ", f_ext)
    random_hex = secrets.token_hex(8)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, book_covers, picture_fn)

    try:
        urllib.request.urlretrieve (url, picture_path)
    except:
        return "error"

    image = Image.open(picture_path)
    w, h = image.size
    wr = 2
    hr = 3
    ratio = wr/hr

    if w > h*ratio:
        print("width larger")
        left = (w - h*(wr/hr))/2
        top = 0
        print("Cropping",left,"from left")
        crop = image.crop((left, top, w-left, h-top))
    else:
        print("height larger")
        top = (h - w*(hr/wr))/2
        left = 0
        print("Cropping",top,"from top")
        crop = image.crop((left, top, w-left, h-top))

    crop.thumbnail([1000, 1500])
    crop.save(picture_path)
    return picture_fn


def delete_book_cover(old_picture):
    global book_covers
    try:
        picture_path = os.path.join(current_app.root_path, book_covers, old_picture)
        os.remove(picture_path)
        return True
    except:
        return False
