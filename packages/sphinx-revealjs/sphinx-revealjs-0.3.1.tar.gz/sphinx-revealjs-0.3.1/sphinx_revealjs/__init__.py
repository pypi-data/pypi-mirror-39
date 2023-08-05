"""
"""

__version__ = '0.3.1'


from sphinx.application import Sphinx

from sphinx_revealjs.builders import RevealjsHTMLBuilder
from sphinx_revealjs.directives import RevealjsSection
from sphinx_revealjs.nodes import revealjs_section
from sphinx_revealjs.themes import get_theme_path
from sphinx_revealjs.writers import not_write


def setup(app: Sphinx):
    app.add_builder(RevealjsHTMLBuilder)
    app.add_node(
        revealjs_section,
        html=(not_write, not_write),
        revealjs=(not_write, not_write))
    app.add_directive('revealjs_section', RevealjsSection)
    app.add_html_theme(
        'sphinx_revealjs', str(get_theme_path('sphinx_revealjs')))
    return {
        'version': __version__,
        'env_version': 1,
        'parallel_read_safe': False,
    }
