from data.RPK_Node import *
from sys import argv, stdout, stderr
import os
import argparse
import json

parser = argparse.ArgumentParser(
    description="Parse Planetfall's RPK file format, and manipulate resulting data"
)
parser.add_argument("-j", "--json", action="store_true")
parser.add_argument("-f", "--filepath", action="store", type=str)


def main():

    parsed_args = parser.parse_args(argv[1:])
    node: RPK_Node = None
    if parsed_args.filepath:
        filepath = parsed_args.filepath
        node = RPK_Node(filepath)
        if parsed_args.json:
            print(node.to_json(), file=stderr)
    else:
        while (filepath := input("Enter full filepath:\n")) != "exit":
            node = RPK_Node(filepath)
            print("-"*40)
            if parsed_args.json:
                print(node.to_json(), file=stderr)


def node_dict_from_filepath(filepath):
    """
    Temporary function to open up the dict as a return so that you can hook in by importing.

    If you want to run the project from another file, import this function and give it a filepath
    :param filepath:
    :return:
    """
    return RPK_Node(filepath).to_dict()


if __name__ == "__main__":
    main()
