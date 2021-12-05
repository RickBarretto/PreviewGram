"""Code adapted from https://github.com/mitmproxy/pdoc/blob/main/docs/make.py
"""

import shutil
import textwrap
from pathlib import Path

import pygments.formatters.html
import pygments.lexers.python
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

import pdoc.render
import pdoc
import pdoc.templates

VERSION = 1.1

here = Path(__file__).parent

if __name__ == '__main__':

    demo = here / ".." / "test" / "testdata" / "demo.py"
    env = Environment(loader=pdoc.templates, autoescape=True)

    lexer = pygments.lexers.python.PythonLexer()
    formatter = pygments.formatters.html.HtmlFormatter(style="friendly")
    pygments_css = formatter.get_style_defs()
    example_html = Markup(pygments.highlight(demo.read_text("utf8"), lexer, formatter))

    (here / "index.html").write_bytes(
        env.get_template("index.html.jinja2").render(
            example_html=example_html,
            pygments_css=pygments_css,
            __version__=pdoc.__version__
        ).encode()
    )

    pdoc.render.configure(
        edit_url_map= {
            "Private PreviewGram": "https://github.com/RickBarretto/PreviewGram/tree/main/src"
        },
        logo="https://raw.githubusercontent.com/RickBarretto/PreviewGram/f0fbfed7d11cc7962d52e8bef4d463a8542e5ba7/assets/PreviewGram.svg",
        footer_text= f"Private PreviewGram {VERSION}"
    )

    pdoc.pdoc(
        "src",
        output_directory=here / "docs"
    )

    with (here / "sitemap.xml").open("w", newline="\n") as f:
        f.write(textwrap.dedent(
            """
            <?xml version="1.0" encoding="utf-8"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
            """
        ).strip())

        for file in here.glob("**/*.html"):
            if file.name.startswith("_"):
                continue
            filename = str(file.relative_to(here).replace("index.html", ""))
            f.write(f"""\n<url><loc>https://rickbarretto.github.io/PreviewGram/{filename}</loc></url>""")
        f.write("""\n</urlset>""")