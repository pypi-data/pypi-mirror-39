from xml.etree import ElementTree
from googletrans import Translator


class InvalidOPMLError(ValueError):
    pass


def translate_opml_tree(tree: ElementTree, lang_out: str, lang_in: str='auto', translator=None):
    root = tree.getroot()

    if root.tag != 'opml':
        raise InvalidOPMLError(f"Root element's tag is not 'opml': {root}")

    body = root['body']

    if not translator:
        translator = Translator()

    for outline in body.iter():
        if outline.tag != 'outline':
            raise InvalidOPMLError(f"Tag is not 'outline' for element in <body>: {outline}")

        text = outline.get('text')

        if text is None:
            raise InvalidOPMLError(f"Outline element missing 'text'")

        translation = translator.translate(text, dest=lang_out, src=lang_in)
        outline.set('text', translation)

    return


def translate_opml_file(file_out: str, lang_out: str,
                        file_in: str=None, lang_in: str='auto',
                        translator: Translator=None):
    if file_in is not None:
        tree = ElementTree.parse(file_in)
    else:
        tree = ElementTree.parse(file_out)

    translate_opml_tree(tree, lang_out, lang_in, translator)

    tree.write(file_out)

    return
