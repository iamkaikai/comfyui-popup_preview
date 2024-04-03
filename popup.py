import psutil
import os
from PIL import Image
import torch
import torchvision.transforms.functional as tf
from pathlib import Path
import tempfile
import random
import folder_paths
import subprocess

node_path = os.path.join(folder_paths.get_folder_paths("custom_nodes")[0], "comfyui-popup_preview")
popup_window_path = os.path.join(node_path, 'window', 'popup_window.py')
python_path = os.path.join(node_path, 'window', 'venv', 'Scripts', 'python.exe')



def openWindows(image_path):
    if os.path.exists(python_path):
        python_running = any(p.info['exe'] == python_path for p in psutil.process_iter(['pid', 'name', 'exe']))
        if os.path.exists(popup_window_path):
            if not python_running:
                subprocess.Popen([python_path, popup_window_path, image_path])
        else:
            print(f'Popup window not exist on: {popup_window_path}')
    else:
        print(f'Python not exist on: {python_path} and this is popup window path {popup_window_path}')

def save_image(img: torch.Tensor, subpath):
    # Check if the batch size is more than 1 (multiple images)
    filename_prefix = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5))
    if len(img.shape) == 4:
        batch_size = img.shape[0]
        for i in range(batch_size):
            filename = f"{filename_prefix}_{i}.png"
            file_path = os.path.join(subpath, filename)
            save_single_image(img[i], file_path)
    else:
        filename = f"{filename_prefix}_{i}.png"
        file_path = os.path.join(subpath, filename)
        save_single_image(img, file_path)

def save_single_image(image: torch.Tensor, path):
    print(f"Image saved at {path}")
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError(f"Input image must have 3 channels and a 3-dimensional shape, but got {image.shape}")
    image = image.permute(2, 0, 1)  # Change from HWC to CHW
    image = image.clamp(0, 1)  # Clamp values
    image = tf.to_pil_image(image)  # Convert to PIL for saving
    image.save(path, format="PNG", compress_level=1)
    openWindows(path)


class PreviewPopup:
    INPUT_TYPES = lambda: { "required": { "image": ("IMAGE",) }, }
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "execute"
    CATEGORY = "ToyxyzTestNodes"

    def execute(self,image: torch.Tensor):

        assert isinstance(image, torch.Tensor)
        OUTPUT_PATH = folder_paths.get_temp_directory()
        save_image(image, OUTPUT_PATH)

        return ()

NODE_CLASS_MAPPINGS = {
    "PreviewPopup": PreviewPopup
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PreviewPopup": "PreviewPopup"
}