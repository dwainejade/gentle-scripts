import os
import json

def get_formatted_content(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data["text"]

def append_to_existing_json(base_json_path, formatted_json_dir):
    print('*** Appending content to existing json ***')

    # Load the base JSON data
    with open(base_json_path, 'r') as f:
        wrapped_data = json.load(f)

    json_filenames = [filename for filename in os.listdir(formatted_json_dir) if filename.endswith(".json")]
    sorted_json_filenames = sorted(json_filenames)

    for filename in sorted_json_filenames:
        json_file_path = os.path.join(formatted_json_dir, filename)
        content_text = get_formatted_content(json_file_path)
        audio_file_name = filename.replace('.json', '.mp3')

        # Find the corresponding page in the wrapped_data
        page_matched = False
        for page in wrapped_data["pages"]:
            if page["audio"].endswith(audio_file_name):
                page_matched = True
                page["content"] = {  # Assuming you want to append to this key
                    "audio": page["audio"],
                    "text": content_text
                }
                break

        if not page_matched:
            print(f"No matching page found for audio: {audio_file_name}")

    # Construct the output file path, saving in the same directory as the base json
    output_file_path = base_json_path
    
    # Write the updated data back to the base file
    with open(output_file_path, 'w') as f:
        json.dump(wrapped_data, f, indent=4)

    print('JSON File Ready:', output_file_path)
