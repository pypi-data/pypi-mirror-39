from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(
    loader=PackageLoader("github_cards", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


def render_cards(**context):
    template = env.get_template("index.html")
    return template.render(**context)
