from jinja2 import Environment, PackageLoader, select_autoescape

from github_cards import filters

env = Environment(
    loader=PackageLoader("github_cards", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)
env.filters["readable_font_color"] = filters.readable_font_color


def render_cards(**context):
    template = env.get_template("index.html")
    return template.render(**context)
