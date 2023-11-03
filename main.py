import os
import shutil
import aligner
import format_json
import excel_extractor
import wrapper

# Prompt the user for the base directory and gentle port
BASE_DIR = input("Please enter the base directory:")
GENTLE_PORT = input("Please enter the port Gentle is running on:")
# hardcoded bas dir and port
# BASE_DIR = '/Users/dmatthew8972/Desktop/strongmind/gentle-scripts/phonics_1_88_a2_i2'
# GENTLE_PORT = '8765'

JSON_DIR = os.path.join(BASE_DIR, 'tmp', 'json')

def create_folders():
    tmp_path = os.path.join(BASE_DIR, 'tmp')
    json_path = os.path.join(tmp_path, 'json')

    # Create tmp folder
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    else:
        print("'tmp' folder already exists at", tmp_path)

    # Create json folder inside tmp
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    else:
        print("'json' folder already exists at", json_path)

    return json_path

def cleanup_files_and_folders():
    print('** Deleting temp files **')
    tmp_path = os.path.join(BASE_DIR, 'tmp')
    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)
    else:
        print("'tmp' folder does not exist.")
        

def main():
    json_path = create_folders()

    # Initialize ReadalongBook class and save data as JSON
    base_dir_name = os.path.basename(BASE_DIR)
    excel_file_path = os.path.join(BASE_DIR, f'{base_dir_name}.xlsx')
    audio_folder_path = os.path.join(BASE_DIR, 'audio')
    book = excel_extractor.ReadalongBook(excel_file_path, audio_folder_path)
    book.save_as_json()
    
    # Call your functions here
    aligner.process_audio_files(BASE_DIR, GENTLE_PORT)
    
    # Get the list of JSON files in the JSON directory
    json_files = [f for f in os.listdir(JSON_DIR) if f.endswith('.json')]
    
    for json_file in json_files:
        # Construct the paths for the input JSON file, input text file, and output file
        input_json_path = os.path.join(JSON_DIR, json_file)
        print(input_json_path)
        input_txt_path = os.path.join(BASE_DIR, 'tmp/text', json_file.replace('.json', '.txt'))
        output_file_path = os.path.join(json_path, json_file)
        
        # Call the format_json_function with the correct arguments
        if os.path.exists(input_txt_path):
            format_json.format_json_function(input_json_path, input_txt_path, output_file_path)
        else:
            print(f"main ~~ Missing text file for: {json_file}")
            
    base_json_path = os.path.join(BASE_DIR, f'{base_dir_name}.json')
    formatted_json_dir = json_path
    wrapper.append_to_existing_json(base_json_path, formatted_json_dir)
    
    # cleanup_files_and_folders()
    
    print('DONE!!')

if __name__ == '__main__':
    main()
