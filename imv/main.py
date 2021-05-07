from typing import List, Iterable, Union
from urllib.parse import quote
from pathlib import Path
import logging
import mimetypes

from flask import Flask, request, make_response, redirect
from flask import render_template

# logging.getLogger("werkzeug").setLevel(logging.ERROR)

here = Path(__file__).parent
app = Flask(
    __name__,
    static_folder=str(here / "static"),
    template_folder=str(here / "templates"),
)

IMG_TYPES = ("png", "jpg", "jpeg", "gif", "webp")
VID_TYPES = ("mp4", "webm")


@app.route("/")
def index():
    path: Path = (
        Path(request.args.get("path", ".")).expanduser().resolve()
    )
    recursive: bool = True if request.args.get("recursive") else False

    listdir = [
        (get_static_link(p.resolve()), p.name)
        for p in path.glob("*")
        if p.is_dir()
    ]

    img_paths = _glob(path, recursive=recursive, exts=IMG_TYPES)
    img_paths = get_static_links(img_paths)

    vid_paths = _glob(path, recursive=recursive, exts=VID_TYPES)
    vid_paths = [(s, mimetypes.guess_type(s)[0]) for s in get_static_links(vid_paths)]

    return render_template(
        "index.html",
        path=str(path),
        parent_link="/?path=" + str(path.parent),
        img_paths=img_paths,
        vid_paths=vid_paths,
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
        path = Path(path.replace("%20", " ")).expanduser()
    except TypeError:
        return NOT_FOUND_RESPONSE

    if not path.exists():
        return NOT_FOUND_RESPONSE

    with path.open("rb") as f:
        data = f.read()

    response = make_response(data)
    response.headers.set("Content-Type", "image/" + path.suffix[1:])

    return response


def get_static_links(paths) -> List[str]:
    return [get_static_link(path) for path in paths]


def get_static_link(path: Union[Path, str]) -> str:
    return "/s?path=" + quote(str(path))


def _glob(
    path: Path, recursive: bool = False, exts: Iterable = IMG_TYPES
) -> List[Path]:
    resources = []
    wildcard = "**/*." if recursive else "*."

    for ext in exts:
        resources.extend(list(path.glob(wildcard + ext)))
        resources.extend(list(path.glob(wildcard + ext.upper())))

    return resources


if __name__ == "__main__":
    app.run(port=7000, debug=True)
