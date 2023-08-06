import click
from .translate import translate_opml_file
import logging
import click_log

click_log.basic_config(logging.getLogger('opml_translate'))

# def list_languages(ctx, _param, value):
#     if not value or ctx.resilient_parsing:
#         return
#     click.echo(f"Languages: {googletrans.LANGUAGES}")
#     ctx.exit()
#     return


@click.command('opml-trans')
@click_log.simple_verbosity_option(logging.getLogger('opml_translate'))
@click.option('--file_out', '-o', required=True, type=click.Path())
@click.option('--lang_out', '-lo', required=True)
@click.option('--file_in', '-i', type=click.Path())
@click.option('--lang_in', '-li')
# @click.option('--languages', is_flag=True, callback=list_languages, expose_value=False, is_eager=True)
def translate_command(*args, **kwargs):
    """
    Example usage:
    opml-trans -i dynalist-2018-12-4.opml -li en -o trans.opml -lo zh-cn
    """

    translate_opml_file(*args, **kwargs)
    return

