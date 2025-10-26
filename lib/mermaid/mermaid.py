import markdown
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

class MermaidExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(MermaidPreprocessor(md), 'mermaid', 175)

class MermaidPreprocessor(Preprocessor):
    MERMAID_RE = re.compile(r'```mermaid(.*?)```', re.DOTALL)

    def run(self, lines):
        text = "\n".join(lines)
        return self.MERMAID_RE.sub(self._convert_mermaid, text).split("\n")

    def _convert_mermaid(self, match):
        mermaid_code = match.group(1).strip()
        return f'<div class="mermaid">\n{mermaid_code}\n</div>'

def makeExtension(**kwargs):
    return MermaidExtension(**kwargs)