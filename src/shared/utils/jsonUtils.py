import json

def write_json(new_data, file_path='../../datasets/extractedJsons/KnessetMembersDetails.json'):
    """this func that write the given data to json file."""
    print(new_data)
    with open(file_path, 'w', encoding="utf8") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)