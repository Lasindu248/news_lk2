import re

import spacy
from utils.xmlx import _

nlp = spacy.load("en_core_web_sm")


class POS:
    NE = 'propn'
    OTHER = 'other'
    PUNCT = 'punct'
    NUM = 'num'


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def get_pos(spacy_pos):
    if spacy_pos in ['PROPN']:
        return POS.NE
    if spacy_pos in ['NUM']:
        return POS.NUM
    if spacy_pos in ['PUNCT']:
        return POS.PUNCT
    return POS.OTHER


def get_combined_nlp(text):
    doc = nlp(clean(text))
    prev_pos = None
    combined_nlp = []
    current_token_texts = []
    for token in doc:
        pos = get_pos(token.pos_)
        text = token.text

        if prev_pos and pos != prev_pos:
            combined_nlp.append({
                'pos': prev_pos,
                'text': ' '.join(current_token_texts),
            })
            current_token_texts = []
        current_token_texts.append(text)
        prev_pos = pos

    if current_token_texts:
        combined_nlp.append({
            'pos': prev_pos,
            'text': ' '.join(current_token_texts),
        })
    return combined_nlp


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
