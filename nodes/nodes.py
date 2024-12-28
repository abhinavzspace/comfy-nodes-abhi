import json
import requests
from pathlib import Path
from urllib.parse import urlparse
import re
from .tools import VariantSupport

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


@VariantSupport()
class InversionDemoLazySwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "switch": ("BOOLEAN",),
                "on_false": ("*", {"lazy": True}),
                "on_true": ("*", {"lazy": True}),
            },
        }

    RETURN_TYPES = ("*",)
    FUNCTION = "switch"

    CATEGORY = "InversionDemo Nodes/Logic"

    def check_lazy_status(self, switch, on_false = None, on_true = None):
        if switch and on_true is None:
            return ["on_true"]
        if not switch and on_false is None:
            return ["on_false"]

    def switch(self, switch, on_false = None, on_true = None):
        value = on_true if switch else on_false
        return (value,)

NUM_IF_ELSE_NODES = 10
@VariantSupport()
class InversionDemoLazyConditional:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        args = {
            "value1": ("*", {"lazy": True}),
            "condition1": ("BOOLEAN", {"forceInput": True}),
        }

        for i in range(1,NUM_IF_ELSE_NODES):
            args["value%d" % (i + 1)] = ("*", {"lazy": True})
            args["condition%d" % (i + 1)] = ("BOOLEAN", {"lazy": True, "forceInput": True})

        args["else"] = ("*", {"lazy": True})

        return {
            "required": {},
            "optional": args,
        }

    RETURN_TYPES = ("*",)
    FUNCTION = "conditional"

    CATEGORY = "InversionDemo Nodes/Logic"

    def check_lazy_status(self, **kwargs):
        for i in range(0,NUM_IF_ELSE_NODES):
            cond = "condition%d" % (i + 1)
            if cond not in kwargs:
                return [cond]
            if kwargs[cond]:
                val = "value%d" % (i + 1)
                if val not in kwargs:
                    return [val]
                else:
                    return []

        if "else" not in kwargs:
            return ["else"]

    def conditional(self, **kwargs):
        for i in range(0,NUM_IF_ELSE_NODES):
            cond = "condition%d" % (i + 1)
            if cond not in kwargs:
                return [cond]
            if kwargs.get(cond, False):
                val = "value%d" % (i + 1)
                return (kwargs.get(val, None),)

        return (kwargs.get("else", None),)
    
    
@VariantSupport()
class InversionDemoLazyIndexSwitch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "index": ("INT", {"default": 0, "min": 0, "max": 9, "step": 1}),
                "value0": ("*", {"lazy": True}),
            },
            "optional": {
                "value1": ("*", {"lazy": True}),
                "value2": ("*", {"lazy": True}),
                "value3": ("*", {"lazy": True}),
                "value4": ("*", {"lazy": True}),
                "value5": ("*", {"lazy": True}),
                "value6": ("*", {"lazy": True}),
                "value7": ("*", {"lazy": True}),
                "value8": ("*", {"lazy": True}),
                "value9": ("*", {"lazy": True}),
            }
        }

    RETURN_TYPES = ("*",)
    FUNCTION = "index_switch"

    CATEGORY = "InversionDemo Nodes/Logic"

    def check_lazy_status(self, index, **kwargs):
        key = "value%d" % index
        if kwargs.get(key, None) is None:
            return [key]

    def index_switch(self, index, **kwargs):
        key = "value%d" % index
        return (kwargs[key],)

@VariantSupport()
class InversionDemoLazyMixImages:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image1": ("IMAGE",{"lazy": True}),
                "image2": ("IMAGE",{"lazy": True}),
                "mask": ("MASK",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "mix"

    CATEGORY = "InversionDemo Nodes/Demo"

    def check_lazy_status(self, mask, image1 = None, image2 = None):
        mask_min = mask.min()
        mask_max = mask.max()
        needed = []
        if image1 is None and (mask_min != 1.0 or mask_max != 1.0):
            needed.append("image1")
        if image2 is None and (mask_min != 0.0 or mask_max != 0.0):
            needed.append("image2")
        return needed

    # Not trying to handle different batch sizes here just to keep the demo simple
    def mix(self, mask, image1 = None, image2 = None):
        mask_min = mask.min()
        mask_max = mask.max()
        if mask_min == 0.0 and mask_max == 0.0:
            return (image1,)
        elif mask_min == 1.0 and mask_max == 1.0:
            return (image2,)

        if len(mask.shape) == 2:
            mask = mask.unsqueeze(0)
        if len(mask.shape) == 3:
            mask = mask.unsqueeze(3)
        if mask.shape[3] < image1.shape[3]:
            mask = mask.repeat(1, 1, 1, image1.shape[3])

        return (image1 * (1. - mask) + image2 * mask,)
