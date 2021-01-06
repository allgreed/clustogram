def produce_graph(cli_json):
    objects = cli_json['kubernetesObjects']
    graph_data = {}
    entities = []

    for ob in objects:
        entity = {}
        entity.setdefault("name", ob["metadata"]["name"])
        entity.setdefault("kind", ob["kind"])
        entity.setdefault("references", [])
        entities.append(entity)

    _find_references(entities, objects)

    graph_data.setdefault("version", cli_json["version"] )
    graph_data.setdefault("entities", entities)

    return graph_data


def _find_references(entities, objects):
    # Find references between objects.
    for entity in entities:
        for object in objects:
            name = object["metadata"]["name"]

            found_references = find_val_in_nested_dict(object, name,
                                               val_to_search=entity["name"])

    # Add references to entities
    for entity in entities:
        refer_to_entity = found_references[entity["name"]]

        for ob_name, ob_key_path in refer_to_entity:

            entity["references"].append(
                {"name": ob_name}
            ) if {"name": ob_name} not in  entity["references"] else  entity["references"]

        # Deployment object
        if entity["kind"] == "Deployment":
            for object in objects:
                if object["metadata"]["name"] == entity["name"]:
                    labels = object["spec"]["template"]["metadata"]["labels"]
                    entity["references"].append(
                        {"name": labels["app"]}
                    )


def find_val_in_nested_dict(nested_dict, name, val_to_search, prior_keys=[], found = {}):
    """Find all possible connection between objects."""

    found.setdefault(val_to_search, [])

    for key, value in nested_dict.items():
        current_key_path = prior_keys + [key]
        key_path_str = ''.join('[\'{}\']'.format(key) for key in current_key_path)

        if isinstance(value, dict):
            find_val_in_nested_dict(value, name, val_to_search, current_key_path, found)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    find_val_in_nested_dict(item, name, val_to_search, current_key_path, found)
        else:
            if key == "name" and value == val_to_search:
                found[val_to_search].append([name, key_path_str])
    return found