import os
import shutil

'''
Meant to take a bunch of folders in a directory, take out the audio segments, and then put them in one folder.
This was a quick script made to combine the segments outputted from the extraction script as they're individual
folders inside dataset/wav_splits
'''

def merge_segments(output_dir):
    combined_dir = os.path.join(output_dir, "combined_folder")
    os.makedirs(combined_dir, exist_ok=True)

    for folder_name in os.listdir(output_dir):
        folder_path = os.path.join(output_dir, folder_name)
        if not os.path.isdir(folder_path) or folder_name == "combined_folder":
            continue

        for segment_name in os.listdir(folder_path):
            segment_path = os.path.join(folder_path, segment_name)
            new_segment_name = f"{folder_name}_{segment_name}"
            new_segment_path = os.path.join(combined_dir, new_segment_name)
            shutil.move(segment_path, new_segment_path)

        os.rmdir(folder_path)  # Remove the original directory after all its segments have been moved

if __name__ == "__main__":
    directory_path = "tortoise_data/finetune_models_6/dataset/wav_splits"
    merge_segments(directory_path)