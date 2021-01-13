#!/usr/bin/env python

import sys
import os.path
import json
import yaml
import hcl
import stringcase


def process_yaml(file):
    return [document for document in yaml.load_all(file, Loader=yaml.FullLoader)]


def process_hcl(file):
    document = hcl.load(file)["resource"]

    k8sObjects = []

    for resource in document:
        resourceNameWithoutKubernetesPrefix = resource[resource.startswith("kubernetes_") and len("kubernetes_"):]
        resourceName = stringcase.pascalcase(resourceNameWithoutKubernetesPrefix).replace("Api", "API")

        resourceData = list(document[resource].values())[0]
        obj = {
            "kind": resourceName,
            **resourceData
        }
        k8sObjects.append(obj)

    return k8sObjects

def process_files(filelist):
    k8sObjects = []

    supportedExtensions = {
        ".yml":  process_yaml,
        ".yaml": process_yaml,
        ".tf":  process_hcl
    }

    for filename in filelist:
        ext = os.path.splitext(filename)[1].lower()
        if ext in supportedExtensions.keys():
            with open(filename) as f:
                k8sObjects.extend(supportedExtensions[ext](f))
        else:
            print(f"Unknown filetype: {filename}", file=sys.stderr)
    return k8sObjects

def main(args):
    filelist = []

    for path in args[1:]:
        if os.path.isfile(path):
            filelist.append(path)
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for name in files:
                    filelist.append(os.path.join(root, name))

    k8sObjects = process_files(filelist)

    print(json.dumps(
        {
        "version": 1,
        "kubernetesObjects": k8sObjects
        }
    ))


if __name__ == "__main__":
    main(sys.argv)