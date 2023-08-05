import asyncio
import logging
from typing import Callable, NamedTuple

from ..settings import BaseSettings
from .connection import lenient_conn

logger = logging.getLogger('atoolbox.db.patch')
patches = []


class Patch(NamedTuple):
    func: Callable
    direct: bool = False


def run_patch(settings: BaseSettings, live, patch_name):
    if patch_name is None:
        logger.info(
            'available patches:\n{}'.format(
                '\n'.join('  {}: {}'.format(p.func.__name__, p.func.__doc__.strip('\n ')) for p in patches)
            )
        )
        return
    patch_lookup = {p.func.__name__: p for p in patches}
    try:
        patch = patch_lookup[patch_name]
    except KeyError:
        logger.error('patch "%s" not found in patches: %s', patch_name, [p.func.__name__ for p in patches])
        return 1

    if patch.direct:
        if not live:
            logger.error('direct patches must be called with "--live"')
            return 1
        logger.info(f'running patch {patch_name} direct')
    else:
        logger.info(f'running patch {patch_name} live {live}')
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_run_patch(settings, live, patch))


async def _run_patch(settings, live, patch: Patch):
    conn = await lenient_conn(settings)
    tr = None
    if not patch.direct:
        tr = conn.transaction()
        await tr.start()
    logger.info('=' * 40)
    try:
        await patch.func(conn, settings=settings, live=live)
    except BaseException:
        logger.info('=' * 40)
        logger.exception('Error running %s patch', patch.func.__name__)
        if not patch.direct:
            await tr.rollback()
        return 1
    else:
        logger.info('=' * 40)
        if patch.direct:
            logger.info('committed patch')
        else:
            if live:
                logger.info('live, committed patch')
                await tr.commit()
            else:
                logger.info('not live, rolling back')
                await tr.rollback()
    finally:
        await conn.close()


def patch(*args, direct=False):
    if args:
        assert len(args) == 1, 'wrong arguments to patch'
        func = args[0]
        assert asyncio.iscoroutinefunction(func), f'"{func} is not a coroutine'
        patches.append(Patch(func=func))
        return func
    else:

        def wrapper(func):
            assert asyncio.iscoroutinefunction(func), f'"{func} is not a coroutine'
            patches.append(Patch(func=func, direct=direct))
            return func

        return wrapper


@patch
async def rerun_sql(conn, settings, **kwargs):
    """
    rerun the contents of settings.sql_path. WARNING: depending on how you've written your sql this may be dangerous.
    """
    # this require you to use "CREATE X IF NOT EXISTS" everywhere
    await conn.execute(settings.sql)
