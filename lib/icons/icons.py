import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

class IconExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'icon_pattern': [r'\?([a-zA-Z0-9_-]+)\?', 'Pattern to match icons'],
        }
        super(IconExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.preprocessors.register(IconPreprocessor(md, self.getConfigs()), 'icon', 175)

class IconPreprocessor(Preprocessor):
    def __init__(self, md, config):
        super().__init__(md)
        self.pattern = re.compile(config['icon_pattern'])

    def run(self, lines):
        new_lines = []
        for line in lines:
            new_line = self.pattern.sub(self.replace_icon, line)
            new_lines.append(new_line)
        return new_lines

    def replace_icon(self, match):
        icon_name = match.group(1)
        return f'<i data-feather="{icon_name}"></i>'

# The function to make the extension
def makeExtension(**kwargs):
    return IconExtension(**kwargs)