from typing import List
import logging
import pathlib

from flask import Flask, request, make_response, redirect
from flask import render_template

logging.getLogger("werkzeug").setLevel(logging.ERROR)

here = pathlib.Path(__file__).parent
app = Flask(
    __name__,
    static_folder=str(here / "static"),
    template_folder=str(here / "templates"),
)


@app.route("/")
def index():
    path: pathlib.Path = (
        pathlib.Path(request.args.get("path", ".")).expanduser().resolve()
    )
    recursive: bool = True if request.args.get("recursive") else False

    listdir = [
        ("/?path=" + str(p.resolve()), p.name) for p in path.glob("*") if p.is_dir()
    ]

    img_paths = glob_all_images(path, recursive=recursive)
    img_paths = get_static_paths(img_paths)

    return render_template(
        "index.html",
        path=str(path),
        img_paths=img_paths,
        recursive=recursive,
        listdir=listdir,
    )


@app.route("/", methods=["POST"])
def index_post():
    path = request.form.get("path")
    recursive = request.form.get("recursive")
    redir_url = f"/?path={path}"
    if recursive:
        redir_url += f"&recursive={recursive}"

    return redirect(redir_url)


NOT_FOUND_RESPONSE = ("Not found", 404)


@app.route("/s")
def s():
    "Static files handler"
    path = request.args.get("path", None)
    try:
        path = pathlib.Path(path.replace("%20", " ")).expanduser()
    except TypeError:
        return NOT_FOUND_RESPONSE

    if not path.exists():
        return NOT_FOUND_RESPONSE

    with path.open("rb") as f:
        data = f.read()

    response = make_response(data)
    response.headers.set("Content-Type", "image/" + path.suffix[1:])

    return response


def get_static_paths(paths) -> List[str]:
    return ["/s?path=" + str(path).replace(" ", "%20") for path in paths]


MEDIA_TYPES = ("png", "jpg", "jpeg", "gif", "webp", "mp4", "webm")


def glob_all_images(path: pathlib.Path, recursive=False) -> List[pathlib.Path]:
    image_list = []

    wildcard = "**/*." if recursive else "*."

    for img_type in MEDIA_TYPES:
        image_list.extend(list(path.glob(wildcard + img_type)))
        image_list.extend(list(path.glob(wildcard + img_type.upper())))

    return image_list


if __name__ == "__main__":
    app.run(port=7000, debug=True)
