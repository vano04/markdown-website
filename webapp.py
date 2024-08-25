import markdown
import os
import re
from os.path import exists
from flask import Flask, render_template, abort
import markdown.extensions.fenced_code
from pygments.formatters import HtmlFormatter
from markdown.extensions import Extension

app = Flask(__name__)

# (List?,Code?,[]MD Extentions)
switch = {
    "home": [False,False,['lib.icons']],
    "blog": [True,True,['lib.icons', 'fenced_code', 'codehilite']],
    "projects": [True,True,['lib.icons', 'fenced_code', 'codehilite']],
    "about": [False,True,['lib.icons', 'fenced_code', 'codehilite']],
    "contact": [False,False,['lib.icons']]
}

@app.route("/")
def root():
    data = {}
    data["page_title"] = "Home"

    with open('content/index/home.md', 'r') as f:
        text = f.read()
        # data["pages"] = get_menu()
        data["list"] = False
        data["html"] = markdown.markdown(text, extensions=switch['home'][2])
        if switch['home'][1]:
                data["html"] = stylize_code(data["html"])

        return render_template('index.html', data=data)

@app.route("/<page>")
def get_page(page):
    if exists("content/index/" + page + ".md"):
        data = {}
        data["page_title"] = "About"

        with open('content/index/' + page + '.md', 'r') as f:
            text = f.read()
            data["list"] = False
            data["html"] = markdown.markdown(text, extensions=switch[page][2])
            if switch[page][0]:
                data["list"] = True
                data["items"] = get_items(page)
            if switch[page][1]:
                data["html"] = stylize_code(data["html"])
        return render_template('index.html', data=data)

@app.route("/<dir>/<page>")
def get_dir_page(dir, page):
    if exists("content/"+ dir +"/" + page + ".md"):
        data = {}

        with open('content/'+ dir +'/' + page + '.md', 'r') as f:
            text = f.read()

            md = markdown.Markdown(extensions=['lib.icons', 'meta', 'fenced_code', 'codehilite'])
            html_content = md.convert(text)

            meta_title = md.Meta.get('title', [None])[0]
            data["page_title"] = meta_title if meta_title else re.sub(r'^\d+\.', '', page.title())

            data["pages"] = get_menu()
            data["list"] = False
            data["html"] = stylize_code(html_content)

            return render_template('index.html', data=data)
    else:
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

def get_menu():
	pages = os.listdir("content/index")
	pages = list(map(lambda page:page.replace(".md", ""), pages))
	return pages

def get_items(dir):
    directory = f"content/{dir}" 
    if exists(directory):
        items = os.listdir(directory)
        meta = []
        for item in items:
             with open(f"content/{dir}/"+item, 'r') as f:
                text = f.read()
                md = markdown.Markdown(extensions=['lib.icons','meta', 'fenced_code', 'codehilite'])
                m = {}
                m['content'] = md.convert(text)
                m['meta'] = md.Meta
                m['path'] = f"{dir}/{item}"[:-3]
                meta.append(m)
        meta = meta[::-1]
        return meta
    return []

def stylize_code(text):
    formatter = HtmlFormatter(style="emacs",full=True,cssclass="codehilite")
    css_string = formatter.get_style_defs()
    md_css_string = "<style>" + css_string + "</style>"
        
    return md_css_string + text

if __name__ == "__main__":
    app.run(host='0.0.0.0')