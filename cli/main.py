#!/usr/bin/env python

import sys
import os.path
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

    return [k8sObjects]


def main(args):
    k8sObjects = []
    for filename in args[1:]:
        with open(filename) as f:
            ext = os.path.splitext(filename)[1].lower()
            if ext in [".yml", ".yaml"]:
                k8sObjects.extend(process_yaml(f))
            elif ext == ".tf":
                k8sObjects.extend(process_hcl(f))
            else:
                print("Unknown filetype")
    print({
        "version": 0.1,
        "kubernetesObjects": k8sObjects
    })


if __name__ == "__main__":
    main(sys.argv)
