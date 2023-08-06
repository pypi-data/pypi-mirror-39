import click
from .translate import translate_opml_file


@click.command(name='opml-trans')
@click.argument('file_out', type=click.Path())
@click.argument('lang_out')
@click.option('--file_in', type=click.Path())
@click.option('--lang_in')
def translate_command(*args, **kwargs):
    translate_opml_file(*args, **kwargs)
    return
