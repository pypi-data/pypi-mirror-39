import sys

from vgscli import _version
from vgscli.api import create_api
from vgscli.config import load_config
from vgscli.routes import dump_all_routes, sync_all_routes, create_all_routes
from vgscli.utils import is_file_accessible, eprint
from vgscli.auth import logout, login, handshake
from vgscli.keyring_token_util import KeyringTokenUtil

token_util = KeyringTokenUtil()


def main(args):
    if args.subparser_name == 'version':
        print(_version.version())
        return

    if args.subparser_name == 'logout':
        logout()
        return

    config_file = load_config()
    if args.subparser_name == 'authenticate':
        login(config_file, args.environment)

    handshake(config_file, args.environment)
    if args.subparser_name == 'route':
        if not args.tenant:
            eprint("Please specify --tenant option.")

        vgs_api = create_api(args.tenant, args.environment, token_util.get_access_token().password)
        if args.dump_all:
            dump = dump_all_routes(vgs_api)
            print(dump)
        if args.sync_all:
            dump_data = sys.stdin.read()
            updated_dump = sync_all_routes(vgs_api, dump_data,
                                           lambda route_id: eprint('Route {} processed'.format(route_id)))
            print(updated_dump)
            eprint("Routes updated successfully for tenant " + args.tenant)
        if args.create_all:
            dump_data = sys.stdin.read()
            updated_dump = create_all_routes(vgs_api, dump_data,
                                             lambda route_id: eprint('Route {} processed'.format(route_id)))
            print(updated_dump)
            eprint("Routes created successfully for tenant " + args.tenant)
