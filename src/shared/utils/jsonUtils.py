import json

def write_json(new_data, file_path):
    """this func that write the given data to json file."""
    with open(file_path, 'w', encoding="utf8") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)