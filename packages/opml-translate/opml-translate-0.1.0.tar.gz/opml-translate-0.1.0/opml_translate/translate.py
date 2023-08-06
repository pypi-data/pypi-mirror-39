from xml.etree import ElementTree
from itertools import islice
import translate
import logging


logger = logging.getLogger(__name__)


class InvalidOPMLError(ValueError):
    pass


def translate_opml_tree(tree: ElementTree, lang_out: str, lang_in: str='auto'):
    class Translator:
        def __init__(self, lang_out, lang_in):
            self.lang_out = lang_out
            self.lang_in = lang_in
            self.translator = translate.Translator(lang_out, lang_in)

        def translate(self, text):
            return self.translator.translate(text)

    root = tree.getroot()

    if root.tag != 'opml':
        raise InvalidOPMLError(f"Root element's tag is not 'opml': {root}")

    body = root.find('body')

    translator = Translator(lang_out, lang_in)

    for i, outline in enumerate(islice(body.iter(), 1, None)):
        if outline.tag != 'outline':
            raise InvalidOPMLError(f"Tag is not 'outline' for element in <body>: {outline}")

        text = outline.get('text')

        if text is None:
            raise InvalidOPMLError(f"Outline element missing 'text'")

        translation = translator.translate(text)
        logger.info(f"Translated outline {i}")

        outline.set('text', translation)

    return


def translate_opml_file(file_out: str, lang_out: str,
                        file_in: str=None, lang_in: str='auto'):
    if file_in is not None:
        tree = ElementTree.parse(file_in)
    else:
        tree = ElementTree.parse(file_out)

    translate_opml_tree(tree, lang_out, lang_in)

    tree.write(file_out)

    return
