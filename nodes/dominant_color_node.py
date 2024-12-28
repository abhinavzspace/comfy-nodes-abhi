from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

class DominantColorNode:
    @staticmethod
    def INPUT_TYPES():
        return {
            "required": {
                "image": ("IMAGE",),
                "clusters": ("INT", {"default": 1, "min": 1, "max": 10}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "calculate_dominant_color"

    CATEGORY = "Image Processing"

    def calculate_dominant_color(self, image, clusters):
        # Convert image to NumPy array
        image = np.array(image)

        # Reshape the image to a list of RGB pixels
        pixels = image.reshape((-1, 3))

        # Perform K-Means clustering to find dominant colors
        kmeans = KMeans(n_clusters=clusters, random_state=0).fit(pixels)

        # Get the cluster centers (dominant colors)
        dominant_color = kmeans.cluster_centers_[0]

        # Convert RGB to HEX
        dominant_color_hex = "#{:02x}{:02x}{:02x}".format(
            int(dominant_color[0]), int(dominant_color[1]), int(dominant_color[2])
        )

        return (dominant_color_hex,)

# Register the node
NODE_CLASS_MAPPINGS = {
    "DominantColorNode": DominantColorNode,
}
