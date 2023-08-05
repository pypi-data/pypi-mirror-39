import logging

import click
import coloredlogs

from rspec.io import Database, open_thermo

logger = logging.getLogger(__name__)

coloredlogs.install(
    level='INFO',
    fmt='%(asctime)s %(module)s[%(process)d] %(levelname)s %(message)s',
    datefmt='%H:%M:%S'
)

@click.group()
@click.option('--path', '-p', type=click.Path(exists=True, dir_okay=False))
@click.pass_context
def main(ctx, path):
    db = Database(path)
    ctx.obj = {
        'db': db
    }
    db.open()

@main.command(help="Delete COMPOUND from the database.")
@click.argument('name', metavar='COMPOUND')
@click.pass_context
def delete(ctx, name):
    db = ctx.obj['db']
    try:
        db.pop(name)
    except KeyError:
        raise ValueError("compound \"{}\" does not exist".format(name))
    finally:
        db.close()

@main.command(name='import', help="Import a spectrum from SOURCE.")
@click.argument('source')
@click.option('--name', '-n', 'alt_name', default=None, 
              help="Alternative name for the new compound.")
@click.option('--format', '-f', type=click.Choice(['thermo']))
@click.pass_context
def _import(ctx, source, alt_name, format):
    if not format:
        format = 'thermo'
    if format == 'thermo':
        name, spectrum = open_thermo(source, parse_name=True)
    else:
        raise ValueError("unknown file format")

    if alt_name:
        name = alt_name
    if not name:
        raise RuntimeError("unable to determine name for the new compound")
    
    db = ctx.obj['db']
    db[name] = spectrum    
    db.close()

@main.command(name='list', help="List saved spectrum in the database.")
@click.pass_context
def _list(ctx, name=None):
    db = ctx.obj['db']
    for i, (key, _) in enumerate(db.items()):
        print(" [{}] {}".format(i, key))
    db.close()
