import pathlib
from typing import List

from flask import Flask, request, make_response, render_template, send_file

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def index_post():
    path = request.form.get("path")
    recursive = request.form.get("recursive")

    img_paths = glob_all_images(path, recursive=recursive)
    img_paths = get_static_paths(img_paths)
    print(img_paths)
    return render_template(
        "index.html", path=path, img_paths=img_paths, recursive=recursive
    )


NOT_FOUND_RESPONSE = ("Not found", 404)


@app.route("/s")
def s():
    path = request.args.get("path", None)
    try:
        path = pathlib.Path(path.replace("%20", " ")).expanduser()
    except TypeError:
        return NOT_FOUND_RESPONSE

    if not path.exists():
        return NOT_FOUND_RESPONSE

    with path.open("rb") as f:
        data = f.read()

    print(path.suffix)
    response = make_response(data)
    response.headers.set("Content-Type", "image/" + path.suffix[1:])

    return response


def get_static_paths(paths) -> List[str]:
    return ["/s?path=" + str(path).replace(" ", "%20") for path in paths]


IMAGE_TYPES = ("png", "jpg", "jpeg", "gif")


def glob_all_images(path, recursive=False) -> List[pathlib.Path]:

    if type(path) == str:
        path = pathlib.Path(path).expanduser()

    image_list = []

    wildcard = "**/*." if recursive else "*."

    for img_type in IMAGE_TYPES:
        image_list.extend(list(path.glob(wildcard + img_type)))
        image_list.extend(list(path.glob(wildcard + img_type.upper())))

    return image_list


if __name__ == "__main__":
    app.run(port=7000, debug=True)
