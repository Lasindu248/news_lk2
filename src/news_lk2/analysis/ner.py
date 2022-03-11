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
    combined_nlp = get_combined_nlp(line)
    rendered_segments = []
    for token in combined_nlp:
        pos = token['pos']
        text = token['text']
        rendered_segments.append(
            _(
                'span',
                text,
                {'class': f'span-nlp span-nlp-{pos}'},
            )
        )
    return _('span', rendered_segments)
