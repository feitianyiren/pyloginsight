#!/usr/bin/env python

from pyloginsight.Connection import Connection, Server, Credentials
from capability import Capability
from group import Group
import argparse


class ServerPlus(Server):
    """ Extends the functionality of the Server class by adding groups, and
    datasets. """

    @property
    def groups(self):
        """ Get a list of groups and their properties. DISCLAIMER: At the time of writing this API was a technical preview. """

        groups = []
        for group in self._get('/groups').json()['groups']:
            capabilities = []

            for capability in group['capabilities']:
                capabilities.append(Capability(id=capability['id']))

            groups.append(
                Group(
                    id=group['id'],
                    name=group['name'],
                    description=group['description'],
                    required=bool(group['required']),
                    editable=bool(group['editable']),
                    capabilities=capabilities
                ))

        return groups


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=False, default=None)
    parser.add_argument('-p', '--password', required=False, default=None)
    parser.add_argument('-P', '--provider', required=False, default=None)
    parser.add_argument('-s', '--server', required=True)
    args = parser.parse_args()

    server = ServerPlus(args.server, verify=False)


    if not args.provider:
        # TODO: Get a list of providers for the user and display them.
        pass


    if args.username and args.password and args.provider:
        server.login(
            username=args.username,
            password=args.password,
            provider=args.provider
        )

    print('\n'.join([str(group) for group in server.groups]))

