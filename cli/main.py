#!/usr/bin/env python

import sys
import yaml


def main(args):
    for filename in args[1:]:
        with open(filename) as f:
            docs = yaml.load_all(f, Loader=yaml.FullLoader)
            for doc in docs:
                print(yaml.dump(doc))


if __name__ == "__main__":
    main(sys.argv)
