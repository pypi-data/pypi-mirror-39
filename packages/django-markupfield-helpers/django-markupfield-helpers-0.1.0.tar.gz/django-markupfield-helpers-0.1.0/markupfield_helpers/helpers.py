import markdown2
from docutils.core import publish_parts
from markupfield.fields import MarkupField


def render_md(markup):
    return markdown2.markdown(markup, extras=[
        'code-friendly',
        'cuddled-lists',
        'fenced-code-blocks',
        'footnotes',
        'tables',
    ])


def render_rest(markup):
    parts = publish_parts(source=markup, writer_name="html4css1")
    return parts["fragment"]


MARKUP_FIELD_TYPES = [
    ('Markdown', render_md),
    ('Markdown Basic', markdown2.markdown),
    ('Plain Text', lambda markup: urlize(linebreaks(escape(markup)))),
    ('reStructuredText', render_rest),
]


class MarkupField(MarkupField):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'default_markup_type': 'Markdown',
            'markup_choices': MARKUP_FIELD_TYPES,
        })
        super().__init__(*args, **kwargs)
