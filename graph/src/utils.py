import json


def get_json_content(json_path):
    """Get json content.

    Args:
        json_path (str): path to json.

    Returns:
        (dict): json content.

    """
    with open(json_path, 'r') as json_bytes:
        content = json.load(json_bytes)
    return content

