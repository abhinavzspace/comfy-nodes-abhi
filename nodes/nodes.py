import json
from pathlib import Path

class UtilLoadJson:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {"default": ""}),
            },
            "optional": {
                "print_to_console": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("JSON",)
    CATEGORY = "Abhi Nodes/Utils"
    FUNCTION = "load_json"

    def load_json(self, file_path: str, print_to_console=False):
        # Open and read the JSON file directly
        with Path(file_path).open("r") as file:
            data = json.load(file)
            if print_to_console:
                print("JSON content:", json.dumps(data, indent=4))

            return (data,)