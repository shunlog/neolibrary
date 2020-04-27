import os
import secrets
from ftplib import FTP
from pathlib import Path
import urllib.request
from itertools import groupby

from flask import current_app as app
from PIL import Image
from neolibrary import graph, book_covers
from neolibrary import book_covers, ftp_user, ftp_password, host_ip, host_dir
from neolibrary.models import Book


def match_book(query, node):
    try:
        dt = graph.run(query).data()
        node = dt[0][node]
        book = Book().wrap(node)
        return book
    except:
        print("Error running query!")

def iter_pages(pages, current_page, left_edge=1, right_edge=1, left_current=1, right_current=1):
    ls = [i for i in range(1,pages+1)]
    ls2 = [i for i in range(current_page-left_current-1, current_page+right_current)]
    for i in range(left_edge,pages-right_edge):
        if i not in ls2:
            ls[i] = None
    ls = [i[0] for i in groupby(ls)]
    return ls

def save_book_cover(new_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(new_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/', book_covers, picture_fn)

    image = Image.open(new_pic)
    cropped = crop_picture(image)
    cropped.save(picture_path)

    if ftp_user and ftp_password and host_ip and host_dir:
        ftp = FTP(host_ip, ftp_user, ftp_password)
        ftp.cwd(host_dir+book_covers)
        with open(picture_path, 'rb') as file:
            ftp.storbinary(f'STOR {picture_fn}', file)

    return picture_fn

def download_book_cover(url):
    global book_covers
    f_ext = "."+url.split(".")[-1]
    print("Extension: ", f_ext)
    if f_ext not in ["png","jpg","jpeg"]:
        return None
    random_hex = secrets.token_hex(8)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, book_covers, picture_fn)

    try:
        urllib.request.urlretrieve (url, picture_path)
    except:
        return None

    image = Image.open(picture_path)
    cropped = crop_picture(image)
    cropped.save(picture_path)
    return picture_fn


def delete_book_cover(filename):
    global book_covers
    try:
        if ftp_user and ftp_password and host_ip and host_dir:
            ftp = FTP(host_ip, ftp_user, ftp_password)
            ftp.cwd(host_dir+book_covers)
            ftp.delete(filename)
        else:
            picture_path = os.path.join(app.root_path, 'static/', book_covers, filename)
            os.remove(picture_path)
            return True
    except:
        return False

def crop_picture(image):
    w, h = image.size
    wr = 2
    hr = 3
    ratio = wr/hr

    if w > h*ratio:
        left = (w - h*(wr/hr))/2
        top = 0
        cropped = image.crop((left, top, w-left, h-top))
    else:
        top = (h - w*(hr/wr))/2
        left = 0
        cropped = image.crop((left, top, w-left, h-top))

    cropped.thumbnail([1000, 1500])
    return cropped
