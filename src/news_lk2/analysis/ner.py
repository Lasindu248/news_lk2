import spacy
from utils.xmlx import _

nlp = spacy.load("en_core_web_sm")


def render_line(line):
    doc = nlp(line)
    return _('span', list(map(
        lambda token: _(
            'span',
            token.text,
            {'class': f'span-nlp span-nlp-{token.pos_.lower()}'},
        ),
        [token for token in doc],
    )))
