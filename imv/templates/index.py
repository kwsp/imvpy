INDEX_TMPL = r"""<!doctype html>
<title>Image Viewer</title>

<a href="/"><h2>Image Viewer</h2></a>

<p>Enter the directory containing images you want to view into the box below</p>

<form method="POST">
    <label for="path">Directory: </label>
    <input name="path" value={{ path }}>
    <label for="recursive">Recursive</label>
    {% if recursive %}
        <input name="recursive" type="checkbox" checked>
    {% else %}
        <input name="recursive" type="checkbox">
    {% endif %}
    <input type="submit" value="View">
</form>

{% if img_paths %}

{% for img_path in img_paths %}

    <a href={{ img_path }}><img src={{ img_path }}></a>

{% endfor %}

{% endif %}
"""
