import os
import sys
import argparse
from textwrap import dedent

from libdevlog import DevlogHttpServer, DevlogConfig

def cmd_args():

    root_parser = argparse.ArgumentParser()
    root_parser.add_argument('path',
                             help="Path to devlog config file",
                             default='devlog.yml')
    subparsers = root_parser.add_subparsers(help='command')

    init_cmd = subparsers.add_parser("init")
    init_cmd.set_defaults(cmd='init')

    run_cmd = subparsers.add_parser("run")
    run_cmd.set_defaults(cmd='run')
    run_cmd.add_argument('--ip', nargs='?', help="IP address to bind to", default='127.0.01')
    run_cmd.add_argument('--port', nargs='?', help="Port to listen to", default=8080, type=int)
    run_cmd.add_argument('--project_assets', action='store_true')

    return root_parser


def do_init(argv):
    '''Create devlog.yml from template to work from'''
    path = os.path.abspath(argv.path)
    if not os.path.exists(path):
        print("Creating ", path)
        with open(path, "wt") as fh:
            fh.write(DevlogConfig.TEMPLATE)


def do_run(argv):
    '''Run server'''

    config = DevlogConfig(argv.path)

    # If specified, load project assets from project folder
    assets_path = None
    if argv.project_assets:
        assets_path = os.path.join(os.path.dirname(__file__), '..')

    server = DevlogHttpServer(config=config, project_folder=assets_path)

    server.start_monitors()

    print("Serving http://%s:%d" % (argv.ip, argv.port))
    server.serve_forever(argv.ip, argv.port)

if __name__ == '__main__':

    # Parse args
    argv = cmd_args().parse_args()

    if argv.cmd == 'init':
        do_init(argv)
    elif argv.cmd == 'run':
        do_run(argv)
    else:
        print("Unknown command")
        sys.exit(1)

