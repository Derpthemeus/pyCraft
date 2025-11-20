#!/usr/bin/env python

import getpass
import sys
import re
import yaml

from minecraft.networking.connection import Connection

def player_thread(hostname, port, username):
    print("Connecting in offline mode...")

    def handle_exception(exc, exc_info):
        print("restarting...")
        connection.disconnect()
        connection.connect()

    connection = Connection(hostname, port, username=username, handle_exception=handle_exception)
    connection.exception_handler(handle_exception)
    connection.connect()

def main():
    with open("config.yaml", 'r') as f:
        config = yaml.safe_load(f)
        for account in config["accounts"]:
            player_thread(config["hostname"], config["port"], account["name"])


    while True:
        try:
            pass
        except KeyboardInterrupt:
            print("Bye!")
            sys.exit()


if __name__ == "__main__":
    main()
