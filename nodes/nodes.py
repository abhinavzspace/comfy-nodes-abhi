import json
import requests
from pathlib import Path
from urllib.parse import urlparse

class UtilLoadJson:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "source": ("STRING", {"default": ""}),
            },
            "optional": {
                "print_to_console": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("JSON",)
    CATEGORY = "Nodes Abhi/Utils"
    FUNCTION = "load_json_source"

    def load_json_source(self, source: str, print_to_console=False):
        """
        Loads JSON data from a URL or a local file path.
        
        :param source: The URL or local file path to load the JSON data from.
        :param print_to_console: If True, prints the JSON content.
        :return: The loaded JSON data.
        """
        # Parse the source to check if it is a URL
        parsed_url = urlparse(source)
        
        if parsed_url.scheme in ['http', 'https']:
            # If the scheme is http or https, treat it as a URL
            response = requests.get(source)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
        else:
            # Otherwise, treat it as a local file path
            file_path = Path(source)
            with file_path.open("r") as file:
                data = json.load(file)
        
        if print_to_console:
            print("JSON content:", json.dumps(data, indent=4))

        return (data,)

            