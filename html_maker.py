from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("novelList"),
    autoescape=select_autoescape()
)

template = env.get_template("html_template.html")


# This class is responsible for creating the content of the html file using jinja2 templating engine
class HtmlMaker:
    def __init__(self, title, data):
        self.title = title
        self.data = data

    def make_html_file(self, file):

        with open(file, "w") as f:
            f.write(template.render(title=self.title, book_list=self.data))
