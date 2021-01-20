import pprint
pp = pprint.PrettyPrinter(indent=1)


class Entity:

    def __init__(self, cli_object):
        self.cli_object = cli_object
        self.name = cli_object["metadata"]["name"]
        self.kind = cli_object["kind"]
        self.namespace = ""
        self.match_labels = {}  # only for Deployment and Service object
        self.label_app = {}
        self.label_role = ''
        self.references = []

        if "namespace" in cli_object["metadata"].keys():
            if cli_object["metadata"]["namespace"] != "default":
                self.namespace = cli_object["metadata"]["namespace"]

        self.label_app = cli_object["metadata"]["labels"]

        # LABELS MATCHER
        if self.kind == "Deployment":
            try:
                self.match_labels = cli_object["spec"]["template"]["metadata"]["labels"]
            except KeyError:
                pass
        elif self.kind == "Service":
            try:
                self.match_labels = cli_object["spec"]["selector"]

            except KeyError:
                pass
        try:
            self.label_role = cli_object["metadata"]["labels"]["role"]
        except KeyError:
            pass

    @property
    def full_name(self):
        """namespace::kind::name  ||   kind::name"""
        return "{}::{}::{}".format(
            self.namespace, self.kind, self.name) if self.namespace else \
            "{}::{}".format(self.kind, self.name)

    @property
    def display_name(self):
        """namespace::name || name"""
        return "{}::{}".format(
            self.namespace, self.name) if self.namespace else self.name

    def add_ref(self, ref):
        """Add new reference."""
        if ref not in self.references:
            self.references.append(ref)

    def get_graph_entity (self):
        """Get entity as a dict with only required keys to produce graph."""
        return {
            "name": self.display_name,
            "kind": self.kind,
            "references": self.references
        }


class Graph:
    def __init__(self, cli_json) -> None:
        """Class instantiation."""
        self.entities = []  # type: List(Entity)
        self.found_references = []  # type: List(dict)
        self.cli_json = cli_json

    @property
    def entities_names(self):
        """Get display names of parsed entities."""
        return [en.display_name for en in self.entities]

    def get_entity_display_name(self, name):
        """Get display name of given entity."""
        for en in self.entities:
            if en.name == name:
                return en.display_name
        raise ValueError

    def get_entities_with_label(self, match):
        """Get entities that have 'match' as a subset of ["metadata"]["labels"].
        To be matched with services and deployment objects."""
        print(match)
        for en in self.entities:
            print(en.label_app)
        return [en.display_name for en in self.entities if match.items() <= en.label_app.items()]

    def get_graph_entities(self):
        """Get entities as a dict to produce graph"""
        return [en.get_graph_entity() for en in self.entities]

    def produce_graph(self):
        """Define entities with references."""
        graph_data = {}

        for ob in self.cli_json['kubernetesObjects']:
            entity = Entity(ob)
            self.entities.append(entity)

        self._find_references()
        #pp.pprint(self.found_references)

        graph_data.setdefault("version", self.cli_json["version"] )
        graph_data.setdefault("entities", self.get_graph_entities())

        pp.pprint(graph_data)
        return graph_data

    def _find_references(self):
        """ Find references between objects.

        Search for entity name in other objects
        and assume it could be a relation between them.

        """
        for entity in self.entities:
            for en_ob in self.entities:
                name = en_ob.cli_object["metadata"]["name"]
                self.found_references = self._find_val_in_nested_dict(
                    en_ob.cli_object, name, searched_val=entity.name)

        self._set_dep_and_serv_references()
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
                ref_ob, ob_name, ob_key_path = referential_set
                if ob_key_path not in paths_to_skip:
                    ref = {"name": ref_ob}
                    if(entity.name == ob_name ) and ref_ob in self.entities_names:
                        entity.add_ref(ref)

            if entity.label_role:
                try:
                    ref_ob = self.get_entity_display_name(entity.label_role)
                    ref = {"name": ref_ob}
                    entity.add_ref(ref)
                except ValueError:
                    continue

    def _set_dep_and_serv_references(self):
        """Set references for deployment an service objects."""
        for entity in self.entities:
            if entity.kind == "Service" or entity.kind == "Deployment":
                en_names = self.get_entities_with_label(entity.match_labels)
                for en_display_name in en_names:
                    if entity.display_name != en_display_name:
                        ref = {"name": en_display_name}
                        entity.add_ref(ref)

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
        searched_keys = ["name", "claimName", "serviceName"]
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
                if (key in searched_keys) and value == searched_val:
                    found.append([searched_val, ob_to_search, key_path_str])
        return found