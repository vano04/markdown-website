import markdown
import os
import re
from os.path import exists
from datetime import datetime
from flask import Flask, render_template, abort
import markdown.extensions.fenced_code
from pygments.formatters import HtmlFormatter
from markdown.extensions import Extension

app = Flask(__name__)

# (List?,Code?,[]MD Extentions)
switch = {
    "home": [False,False,['lib.icons', 'sane_lists', 'nl2br', 'admonition']],
    "worklogs": [True,True,['lib.icons', 'footnotes', 'lib.mermaid', 'meta', 'fenced_code', 'codehilite', 'sane_lists', 'nl2br', 'admonition']],
    "projects": [True,True,['lib.icons', 'footnotes', 'lib.mermaid', 'meta', 'fenced_code', 'codehilite', 'sane_lists', 'nl2br', 'admonition']],
    "testing": [True,True,['lib.icons', 'footnotes', 'lib.mermaid', 'meta', 'fenced_code', 'codehilite', 'sane_lists', 'nl2br', 'admonition']],
    "about": [False,True,['lib.icons', 'fenced_code', 'codehilite', 'sane_lists', 'nl2br', 'lib.mermaid', 'admonition']],
    "contact": [False,False,['lib.icons', 'sane_lists', 'nl2br', 'admonition']]
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
        data["page_title"] = page.title()

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
    else:
        abort(404)

@app.route("/<dir>/<page>")
def get_dir_page(dir, page):
    if exists("content/"+ dir +"/" + page + ".md"):
        data = {}

        with open('content/'+ dir +'/' + page + '.md', 'r') as f:
            text = f.read()

            if dir in ("worklogs", "projects", "testing"):
                md = markdown.Markdown(extensions=switch[dir][2])
            else:
                md = markdown.Markdown(extensions=[
                    'lib.icons',
                    'lib.mermaid',
                    'meta',
                    'fenced_code',
                    'codehilite',
                    'sane_lists',
                    'nl2br',
                    'admonition'])
            html_content = md.convert(text)

            meta_title = md.Meta.get('title', [None])[0]
            data["page_title"] = meta_title if meta_title else re.sub(r'^\d+\.', '', page.title())

            # data["pages"] = get_menu()
            data["list"] = False
            data["html"] = stylize_code(html_content)

            return render_template('index.html', data=data)
    else:
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

# def get_menu():
# 	pages = os.listdir("content/index")
# 	pages = list(map(lambda page:page.replace(".md", ""), pages))
# 	return pages

def extract_date_from_metadata(text):
    """
    Extract date in MM/DD/YYYY format from markdown metadata.
    Returns a datetime object or None if no date found.
    """
    # Look for the Date: line in the metadata
    date_pattern = r'Date:\s*(\d{1,2})/(\d{1,2})/(\d{4})'
    match = re.search(date_pattern, text)
    
    if match:
        month, day, year = match.groups()
        try:
            return datetime(int(year), int(month), int(day))
        except ValueError:
            pass
    
    # If no date found, return None or a default date
    return datetime(1970, 1, 1)

# Old by file name. i.e. 1.md 2.md
# def get_items(dir):
#     directory = f"content/{dir}" 
#     if exists(directory):
#         items = os.listdir(directory)
#         meta = []
#         for item in items:
#              with open(f"content/{dir}/"+item, 'r') as f:
#                 text = f.read()
#                 md = markdown.Markdown(extensions=switch[dir][2])
#                 m = {}
#                 m['content'] = md.convert(text)
#                 m['meta'] = md.Meta
#                 m['path'] = f"{dir}/{item}"[:-3]
#                 meta.append(m)
#         meta = meta[::-1]
#         return meta
#     return []

def get_items(dir):
    directory = f"content/{dir}" 
    if exists(directory):
        items = os.listdir(directory)
        meta = []
        for item in items:
            with open(f"content/{dir}/"+item, 'r') as f:
                text = f.read()
                md = markdown.Markdown(extensions=switch[dir][2])
                m = {}
                m['content'] = md.convert(text)
                m['meta'] = md.Meta
                m['path'] = f"{dir}/{item}"[:-3]
                
                # Extract and store the date for sorting
                m['date'] = extract_date_from_metadata(text)
                
                meta.append(m)
        
        # Sort items by date in descending order
        meta.sort(key=lambda x: x['date'], reverse=True)
        
        return meta
    return []

def stylize_code(text):
    formatter = HtmlFormatter(style="tango",full=True,cssclass="codehilite")
    css_string = formatter.get_style_defs()
    md_css_string = "<style>" + css_string + "</style>"
        
    return md_css_string + text

if __name__ == "__main__":
    app.run(host='0.0.0.0')
