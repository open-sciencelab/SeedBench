import os
import json
import argparse

def update_data(source_file, target_file):
    """
    Update the target file with data from the source file.
    If the target file does not exist, it will be created.
    """
    if not os.path.exists(target_file):
        with open(target_file, 'w') as f:
            json.dump([], f)  # Create an empty list if the file does not exist

    with open(source_file, 'r') as f:
        update_data = json.load(f)

    with open(target_file, 'r') as f:
        target_data = json.load(f)

    print(f"Before update: {len(target_data)} items in {target_file}")
    target_data.extend(update_data)
    print(f"After update: {len(target_data)} items in {target_file}")

    return target_data

def deduplicate_data(data):
    """
    Deduplicate the data based on 'instruction' and 'question'.
    """
    seen = set()
    deduplicated_data = []
    for item in data:
        key = (item['instruction'], item['question'])
        if key not in seen:
            seen.add(key)
            deduplicated_data.append(item)
    print(f"Deduplicated data: {len(deduplicated_data)} items")
    return deduplicated_data

def save_data(data, target_file):
    """
    Save the data to the target file.
    """
    with open(target_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {target_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Update and deduplicate data files.")
    parser.add_argument('--src_dir', type=str, required=True, help='Source directory containing the data files.')
    parser.add_argument('--target_dir', type=str, required=True, help='Target directory to save the updated data files.')

    args = parser.parse_args()
    src_dir = args.src_dir
    target_dir = args.target_dir

    folders = ['one-shot', 'zero-shot']
    for folder in folders:
        for src_file in os.listdir(os.path.join(src_dir, folder)):
            if src_file.endswith('.json'):
                src_file_path = os.path.join(src_dir, folder, src_file)
                target_file_path = os.path.join(target_dir, folder, src_file)
                print(f"Updating {target_file_path} with data from {src_file_path}")
                updated_data = update_data(src_file_path, target_file_path)
                deduplicated_data = deduplicate_data(updated_data)
                save_data(deduplicated_data, target_file_path)
    print("Data update completed.")

