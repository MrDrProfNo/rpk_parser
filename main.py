from data.RPK_Node import *
from sys import argv, stdout
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
            if node is None:
                raise
            print(node.__dict__)
    else:
        while (filepath := input("Enter full filepath:\n")) != "exit":
            node = RPK_Node(filepath)
            print("-"*40)
            if parsed_args.json:
                if node is None:
                    raise
                print(node.__dict__)



if __name__ == "__main__":
    main()
