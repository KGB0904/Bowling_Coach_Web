import os

def get_next_output_folder(base_dir, base_folder_name="folder"):
    counter = 1
    while True:
        folder_name = f"{base_folder_name}_{counter}"
        output_folder = os.path.join(base_dir, "output_frame", folder_name)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            return output_folder
        counter += 1


