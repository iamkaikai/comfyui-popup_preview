import os
import sys
import json
import folder_paths
import time

node_path = os.path.join(folder_paths.get_folder_paths("custom_nodes")[0], "comfyui-popup_preview")
popup_window_path = os.path.join(node_path, 'window', 'popup_window.py')
ps_gui_path = os.path.join(node_path, 'window', 'ps_gui.py')
python_path = os.path.join(node_path, 'window', 'venv', 'Scripts', 'python.exe')

sys.path.append(node_path)
from ps_gui import popup_GUI
sys.path.remove(node_path)


# my_dir = os.path.dirname(os.path.abspath(__file__))
# comfy_dir = os.path.abspath(os.path.join(my_dir, '..', '..'))
# sys.path.append(comfy_dir)
# import comfy.controlnet
# sys.path.remove(comfy_dir)


class PreviewPopup:
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required": { 
                    "input_data_path": ("STRING", {"default": "user_input_data.json"}),
                    "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),   #make sure the server refresh the seed to update the values from user_input_data
                },
            }
    RETURN_TYPES = ("denoise", "noise_type", "noise_scale", "reverse_CADS", "batch_size", "positive", "negative", "lora_name", "LACE_step", "steps", "strength", "control_net_name")
    RETURN_NAMES = ("denoise", "noise_type", "noise_scale", "reverse_CADS", "batch_size", "positive", "negative", "lora_name", "LACE_step", "steps", "strength", "control_net_name")
    FUNCTION = "execute"
    CATEGORY = "LACE/Visualization"
    
    def handle_submit(self, data):
        # Handle the received data
        self.data_received = data

    def execute(self, input_data_path=None, seed=None):
        reverse_CADS = False
        with open(input_data_path, 'r') as f:
            user_input_data = json.load(f)

        if user_input_data['reverse_CADS'] == "Radical":
            print("Reverse CADS")
            reverse_CADS = True
       
        return (
            user_input_data['denoise'],
            user_input_data['noise_type'],
            user_input_data['noise_scale'],
            reverse_CADS,
            user_input_data['num_output'],
            user_input_data['prompt_positive'],
            user_input_data['prompt_negative'],
            user_input_data['lora_model'],
            user_input_data['visualized_steps'],
            user_input_data['sampling_steps'],
            user_input_data['strength'],
            user_input_data['cnet_model']
        )
    

NODE_CLASS_MAPPINGS = {
    "PreviewPopup_GUI": PreviewPopup
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PreviewPopup_GUI": "PreviewPopup_GUI"
}