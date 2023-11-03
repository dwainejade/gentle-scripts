import os
import requests
import shutil

def process_audio_files(base_dir, gentle_port):
    # Paths
    tmp_dir = os.path.join(base_dir, "tmp")
    json_dir = os.path.join(tmp_dir, "json")
    tmp_text_dir = os.path.join(tmp_dir, "tmp_text")
    cleaned_text_dir = os.path.join(tmp_dir, "cleaned_text")
    audio_dir = os.path.join(base_dir, "audio")
    text_dir = os.path.join(base_dir, "tmp/text")

    # Create directories
    os.makedirs(json_dir, exist_ok=True)
    os.makedirs(tmp_text_dir, exist_ok=True)
    os.makedirs(cleaned_text_dir, exist_ok=True)

    # Process audio files
    for audio_file in os.listdir(audio_dir):
        if audio_file.endswith(".mp3"):
            base_name = os.path.splitext(audio_file)[0]
            print(f'*** processing {base_name} audio ***')
            
            # Check if the corresponding text file in the text directory is a .txt or .rtf
            txt_file_path = os.path.join('tmp', text_dir, f"{base_name}.txt")
            if os.path.exists(txt_file_path):
                txt_file = txt_file_path
            else:
                print(f"No corresponding text file found for {base_name} in the text directory.")
                continue
            
            # Clean the text file and save to the cleaned text directory
            with open(txt_file, "r") as f:
                content = f.read().replace("#", "").replace("/", "")
            cleaned_txt_path = os.path.join(cleaned_text_dir, f"{base_name}.txt")
            with open(cleaned_txt_path, "w") as f:
                f.write(content)
            
            # Call Gentle aligner and save the output to the json directory using the cleaned text
            audio_path = os.path.join(audio_dir, audio_file)
            response = requests.post(f"http://localhost:{gentle_port}/transcriptions?async=false",
                                    files={'audio': (audio_file, open(audio_path, 'rb')),
                                            'transcript': (f"{base_name}.txt", open(cleaned_txt_path, 'r'))})
            json_path = os.path.join(json_dir, f"{base_name}.json")
            with open(json_path, "w") as f:
                f.write(response.text)

    # Cleanup the temporary text and cleaned text directories
    # shutil.rmtree(tmp_text_dir)
    # shutil.rmtree(cleaned_text_dir)