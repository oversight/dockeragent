import argparse
import asyncio

from setproctitle import setproctitle
from lib.agent import Agent
from lib.check import CHECKS
from lib.logger import setup_logger
from lib.version import __version__


if __name__ == '__main__':
    setproctitle('dockeragent')

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-l', '--log-level',
        default='warning',
        help=(
            'set the log level or use the environment variable OSDA_LOG_LEVEL'
        ),
        choices=['debug', 'info', 'warning', 'error'])

    parser.add_argument(
        '--log-colorized',
        action='store_true',
        help='use colorized logging')

    args = parser.parse_args()

    setup_logger(args.log_level, args.log_colorized)

    cl = Agent(
        'dockeragent',
        __version__,
        CHECKS,
    )

    asyncio.get_event_loop().run_until_complete(
        cl.run_agent()
    )
