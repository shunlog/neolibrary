import os
import secrets
from ftplib import FTP
from pathlib import Path

from PIL import Image
from neolibrary import  profile_pics, ftp_user, ftp_password, host_ip, host_dir
from flask import current_app as app

def crop_n_resize(pic):
    width, height = pic.size
    left = 0 if width < height else (width-height)/2
    right = width - left
    top =  0 if height < width else (height-width)/2
    bottom = height - top
    pic= pic.crop((left, top, right, bottom))
    pic = pic.resize([250, 250])
    return pic


def save_profile_pic(new_pic):
    global profile_pics
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(new_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/', profile_pics, picture_fn)

    smaller_pic= Image.open(new_pic)
    smaller_pic= crop_n_resize(smaller_pic)
    smaller_pic.save(picture_path)

    if ftp_user and ftp_password and host_ip and host_dir:
        ftp = FTP(host_ip, ftp_user, ftp_password)
        ftp.cwd(host_dir+profile_pics)
        with open(picture_path, 'rb') as file:
            ftp.storbinary(f'STOR {picture_fn}', file)

    return picture_fn


def delete_profile_pic(old_picture):
    global profile_pics
    try:
        if ftp_user and ftp_password and host_ip and host_dir:
            ftp = FTP(host_ip, ftp_user, ftp_password)
            ftp.cwd(host_dir+profile_pics)
            ftp.delete(filename)
        else:
            picture_path = os.path.join(app.root_path, 'static/', profile_pics, old_picture)
            os.remove(picture_path)
    except:
        pass
