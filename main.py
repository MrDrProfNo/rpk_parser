from data.RPK_Node import *
from sys import argv
import os

def main():
    if len(argv) > 1:
        for file_path in argv[1:]:
            node: RPK_Node = RPK_Node(file_path)
    else:
        while (file_path := input("Enter full filepath:\n")) != "exit":
            node: RPK_Node = RPK_Node(file_path)
            print("-"*40)

if __name__ == "__main__":
    main()
