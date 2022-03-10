import spacy
from utils.xmlx import _

nlp = spacy.load("en_core_web_sm")


def render_line(line):
    doc = nlp(line)
    prev_pos = None
    current_segment = None
    rendered_segments = []
    for token in doc:
        pos = token.pos_.lower()
        text = token.text
        if pos != prev_pos:
            rendered_segments.append(
                _(
                    'span',
                    current_segment,
                    {'class': f'span-nlp span-nlp-{prev_pos}'},
                )
            )
            current_segment = None

        if current_segment is None:
            current_segment = text
        else:
            current_segment += ' ' + text
        prev_pos = pos

    if current_segment:
        rendered_segments.append(
            _(
                'span',
                text,
                {'class': f'span-nlp span-nlp-{prev_pos}'},
            )
        )
    return _('span', rendered_segments)
