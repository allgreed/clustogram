#!/usr/bin/env python

import sys
import yaml
import os.path


def process_yaml(file):
    return [document for document in yaml.load_all(file, Loader=yaml.FullLoader)]


def process_hcl(file):
    pass


def main(args):
    k8sObjects = []
    for filename in args[1:]:
        with open(filename) as f:
            ext = os.path.splitext(filename)[1].lower()
            if ext in [".yml", ".yaml"]:
                k8sObjects.append(process_yaml(f))
            elif ext == ".tf":
                k8sObjects.append(process_hcl(f))
            else:
                print("Unknown filetype")
    print({
        "version": 0.1,
        "kubernetesObjects": k8sObjects
    })


if __name__ == "__main__":
    main(sys.argv)
