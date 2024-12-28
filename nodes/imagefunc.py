import numpy as np
from PIL import Image, ImageFilter
import colorsys

def log(message, message_type='info'):
    """Logs messages with type."""
    print(f"[{message_type.upper()}] {message}")

def tensor2pil(tensor):
    """Converts a PyTorch tensor to a PIL image."""
    array = tensor.squeeze().detach().cpu().numpy()
    array = np.transpose(array, (1, 2, 0))  # Convert CHW to HWC
    array = (array * 255).clip(0, 255).astype(np.uint8)
    return Image.fromarray(array)

def gaussian_blur(image, radius):
    """Applies Gaussian blur to the PIL image."""
    return image.filter(ImageFilter.GaussianBlur(radius))

def get_image_color_tone(image):
    """Extracts the main color tone from the image."""
    pixels = np.array(image)
    pixels = pixels.reshape(-1, 3)
    colors, counts = np.unique(pixels, axis=0, return_counts=True)
    main_color = colors[np.argmax(counts)]
    return f"#{main_color[0]:02x}{main_color[1]:02x}{main_color[2]:02x}"

def get_image_color_average(image):
    """Calculates the average color of the image."""
    pixels = np.array(image)
    avg_color = pixels.mean(axis=(0, 1))
    return f"#{int(avg_color[0]):02x}{int(avg_color[1]):02x}{int(avg_color[2]):02x}"

def RGB_to_HSV(rgb):
    """Converts RGB to HSV."""
    r, g, b = rgb
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return [h * 360, s * 100, v * 100]

def Hex_to_RGB(hex_color):
    """Converts HEX color to RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
