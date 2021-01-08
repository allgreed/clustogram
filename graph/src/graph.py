class Graph:

    def __init__(self, cli_json) -> None:
        """Class instantiation."""
        self.entities = [] # type: List
        self.found_references = []  # type: List
        self.cli_json = cli_json
        self.cli_objects = cli_json['kubernetesObjects']  # type: List

    @property
    def entities_names(self):
        """Names of parsed entities."""
        names = []
        for entity in self.entities:
            names.append(entity["name"])
        return names

    def produce_graph(self):
        """Define entities with references."""
        graph_data = {}

        for ob in self.cli_objects:
            entity = {}
            entity.setdefault("name", ob["metadata"]["name"])
            entity.setdefault("kind", ob["kind"])
            self.entities.append(entity)

        self._find_references()

        graph_data.setdefault("version", self.cli_json["version"] )
        graph_data.setdefault("entities", self.entities)

        return graph_data

    def _find_references(self):
        """ Find references between objects.

        Search for entity name in other objects
        and assume it could be arelation between them.

        """
        for entity in self.entities:
            entity.setdefault("references", [])
            for object in self.cli_objects:
                name = object["metadata"]["name"]
                self.found_references = self._find_val_in_nested_dict(
                    object, name, searched_val=entity["name"])
        self._set_service_references()
        self._set_deployment_references()
        self._set_base_references()

    def _set_base_references(self):
        """Set references for all type objects."""
        paths_to_skip = [
            "['metadata']['labels']['name']",
            "['metadata']['name']",
            "['spec']['template']['metadata']['labels']['name']",  # deployment
            "['spec']['selector']['matchLabels']['name']"  # deployment
        ]
        for entity in self.entities:
            for referential_set in self.found_references:
                ref_ob, ob_name, ob_key_path=referential_set
                if ob_key_path not in paths_to_skip:
                    if entity["name"] == ob_name and ref_ob in self.entities_names:
                        entity["references"].append(
                            {"name": ref_ob})

    def _set_deployment_references(self):
        """Set references for deployment objects."""
        for entity in self.entities:
            if entity["kind"] == "Deployment":
                ob = self.get_ob_by_name(name=entity["name"])
                labels = ob["spec"]["template"]["metadata"]["labels"]
                if labels["app"] in self.entities_names:
                    entity["references"].append(
                        {"name": labels["app"]})

    def _set_service_references(self):
        """Set references for service objects."""
        for entity in self.entities:
            if entity["kind"] == "Service":
                ob = self.get_ob_by_name(entity["name"])
                labels = ob["spec"]["selector"]
                if labels["app"] in self.entities_names:
                    entity["references"].append(
                        {"name": labels["app"]}
                    )

    def get_ob_by_name(self, name):
        """Get the object from objects list."""
        for ob in self.cli_objects:
            if ob["metadata"]["name"] == name:
                return ob
            else:
                None

    def _find_val_in_nested_dict(self, nested_dict, ob_to_search, searched_val, prior_keys=[], found = []):
        """Find all occurrences of a given object name in a set of objects.

        Args:
            nested_dict (dict): objects database to search.
            ob_to_search (str): object name to be search.
            searched_val (str): name to be found in given object.
            prior_keys (list): key path chain.
            found (list): set of founded occurrences [searched_val, ob_to_search, key_path_str]

        Returns:
            found (list): set of founded occurrences [searched_val, ob_to_search, key_path_str]
        """
        for key, value in nested_dict.items():
            current_key_path = prior_keys + [key]
            key_path_str = ''.join('[\'{}\']'.format(key) for key in current_key_path)
            if isinstance(value, dict):
                self._find_val_in_nested_dict(value, ob_to_search, searched_val, current_key_path, found)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._find_val_in_nested_dict(item, ob_to_search, searched_val, current_key_path, found)
            else:
                if key == "name" and value == searched_val:
                    found.append([searched_val, ob_to_search, key_path_str])
        return found