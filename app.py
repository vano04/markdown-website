import markdown
import os
import re
from os.path import exists
from flask import Flask, render_template, abort
# import markdown.extensions.fenced_code
from markdown.extensions import Extension

app = Flask(__name__)

@app.route("/")
def root():
    data = {}
    data["page_title"] = "Home"

    with open('content/home.md', 'r') as f:
        text = f.read()
        data["pages"] = get_menu()
        data["html"] = markdown.markdown(text, extensions=['lib.icons'])

    return render_template('index.html', data=data)

@app.route("/about")
def about():
    data = {}
    data["page_title"] = "About"

    with open('content/index/about.md', 'r') as f:
        text = f.read()
        data["pages"] = get_menu()
        data["list"] = False
        data["html"] = markdown.markdown(text, extensions=['lib.icons'])

    return render_template('index.html', data=data)

@app.route("/contact")
def contact():
    data = {}
    data["page_title"] = "Contact"

    with open('content/index/contact.md', 'r') as f:
        text = f.read()
        data["pages"] = get_menu()
        data["list"] = False
        data["html"] = markdown.markdown(text, extensions=['lib.icons'])

    return render_template('index.html', data=data)

@app.route("/projects")
def projects():
    data = {}
    data["page_title"] = "Projects"

    with open('content/index/projects.md', 'r') as f:
        text = f.read()
        data["pages"] = get_menu()
        data["list"] = True
        data["items"] = get_items("projects")
        data["html"] = markdown.markdown(text, extensions=['lib.icons'])

    return render_template('index.html', data=data)

@app.route("/blog")
def blog():
    data = {}
    data["page_title"] = "Blog"

    with open('content/index/blog.md', 'r') as f:
        text = f.read()
        data["pages"] = get_menu()
        data["list"] = True
        data["items"] = get_items("blog")
        data["html"] = markdown.markdown(text, extensions=['lib.icons'])
        
    return render_template('index.html', data=data)

@app.route("/<dir>/<page>")
def get_blog_page(dir, page):
    if exists("content/"+ dir +"/" + page + ".md"):
        data = {}

        with open('content/'+ dir +'/' + page + '.md', 'r') as f:
            text = f.read()

            md = markdown.Markdown(extensions=['lib.icons', 'meta'])
            html_content = md.convert(text)

            meta_title = md.Meta.get('title', [None])[0]
            data["page_title"] = meta_title if meta_title else re.sub(r'^\d+\.', '', page.title())

            data["pages"] = get_menu()
            data["list"] = False
            data["html"] = html_content

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
                md = markdown.Markdown(extensions=['lib.icons','meta'])
                m = {}
                m['content'] = md.convert(text)
                m['meta'] = md.Meta
                m['path'] = f"{dir}/{item}"[:-3]
                meta.append(m)
        meta = meta[::-1]
        return meta
    return []