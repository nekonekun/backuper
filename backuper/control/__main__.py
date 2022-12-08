import logging

import asyncclick as click
import pathlib

from backuper.control.parser import load_config_objects
from backuper.control.crud import create_entry_from_object, delete_all_entries
from backuper.db.session import get_async_session
from backuper.errors import ParseError


@click.group()
@click.option(
    '-d', '--database',
    type=str,
    envvar='BACKUPER_DATABASE',
    required=True
)
@click.pass_context
def main(ctx, database):
    ctx.ensure_object(dict)
    ctx.obj['database'] = database


@click.command()
@click.option(
    '--folder', '-F',
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=True
)
@click.pass_context
async def reload(ctx, folder):
    cfg_folder = pathlib.Path(folder)
    # session = get_async_session(ctx.obj['database'])()
    sessionmaker = get_async_session(ctx.obj['database'])
    async with sessionmaker() as session:
        async with session.begin():
            await delete_all_entries(session)
    for filepath in sorted(list(cfg_folder.iterdir())):
        print(filepath)
        try:
            new_objs = load_config_objects(str(filepath))
        except ParseError as err:
            logging.error('Error occurred while parsing file {}: {}'.
                          format(filepath, err))
            continue
        async with sessionmaker() as session:
            async with session.begin():
                for obj in new_objs:
                    session.add(obj)
                await session.flush()


@click.command()
@click.pass_context
async def show(ctx):
    pass


@click.command()
@click.option(
    '--file', '-f',
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    multiple=True
)
@click.option(
    '--folder', '-F',
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    multiple=True
)
@click.pass_context
async def load(ctx, file, folder):
    sessionmaker = get_async_session(ctx.obj['database'])
    for filepath in file:
        try:
            new_objs = load_config_objects(str(filepath))
        except ParseError as err:
            logging.error('Error occurred while parsing file {}: {}'.
                          format(filepath, err))
            continue
        async with sessionmaker() as session:
            async with session.begin():
                for obj in new_objs:
                    session.add(obj)
    for folderpath in folder:
        cfg_folder = pathlib.Path(folderpath)
        for filepath in cfg_folder.iterdir():
            try:
                new_objs = load_config_objects(str(filepath))
            except ParseError as err:
                logging.error('Error occurred while parsing file {}: {}'.
                              format(filepath, err))
                continue
            async with sessionmaker() as session:
                async with session.begin():
                    for obj in new_objs:
                        session.add(obj)


main.add_command(reload)
main.add_command(show)
main.add_command(load)
