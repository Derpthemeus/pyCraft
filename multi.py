#!/usr/bin/env python

import getpass
import sys
import re
import yaml
import uuid

from minecraft.networking.connection import Connection

def handle_exception(connection):
    def _handle_exception(exc, exc_info):
        print("restarting...")
        connection.disconnect()
        connection.connect()
    return _handle_exception


def player_thread(hostname, port, username, uuid):
    print("Connecting in offline mode...")



    connection = Connection(hostname, port, username=username, uuid=uuid)
    connection.exception_handler(handle_exception(connection))
    connection.connect()

def main():
    with open("config.yaml", 'r') as f:
        config = yaml.safe_load(f)
        for account in config["accounts"]:
            player_thread(config["hostname"], config["port"], account["name"], config["uuid"] if "uuid" in config else str(uuid.uuid4()))


    while True:
        try:
            pass
        except KeyboardInterrupt:
            print("Bye!")
            sys.exit()


if __name__ == "__main__":
    main()
