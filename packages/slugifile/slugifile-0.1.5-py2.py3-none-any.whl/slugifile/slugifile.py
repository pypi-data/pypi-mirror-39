# -*- coding: utf-8 -*-
from slugify import slugify

import os


"""Main module."""


def ascii_safe_filename(filename: str) -> dict:
    file = os.path.splitext(filename)
    slug = slugify(file[0], separator="_")
    ext = file[1]

    return {"f_in": filename, "f_out": "{}{}".format(slug, ext)}


def slugifile_directory(path: str):
    success = True
    messages = []

    if path is None:
        success = False
        messages.append("No path specified. Done.")
    else:
        path = path.rstrip("\\/")
        if not os.path.isdir(path):
            success = False
            messages.append("Path specified is not a directory. Done.")
        else:
            filenames = os.listdir(path)
            for filename in filenames:
                result = ascii_safe_filename(filename)

                f_in = result["f_in"]
                f_out = result["f_out"]

                if f_in == f_out:
                    messages.append("Skipping: {}".format(f_in))
                    continue

                filename_in = "{}/{}".format(path, f_in)
                filename_out = "{}/{}".format(path, f_out)

                messages.append("Renaming: {} => {}".format(f_in, f_out))
                os.rename(filename_in, filename_out)

    return {"success": success, "messages": messages}
