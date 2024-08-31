from .nodes.nodes import *

NODE_CLASS_MAPPINGS = { 
    "Load Json File": UtilLoadJson,
    "InversionDemoLazySwitch": InversionDemoLazySwitch,
    "InversionDemoLazyIndexSwitch": InversionDemoLazyIndexSwitch,
    "InversionDemoLazyMixImages": InversionDemoLazyMixImages,
    "InversionDemoLazyConditional": InversionDemoLazyConditional,
}
    
print("\033[34mComfyUI Nodes Abhi: \033[92mLoaded\033[0m")