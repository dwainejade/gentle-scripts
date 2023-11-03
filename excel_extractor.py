import pandas as pd
import os
import json

class ReadalongBook:
    def __init__(self, excel_file_path, audio_folder_path):
        self.excel_file_path = excel_file_path
        self.audio_folder_path = audio_folder_path
        self.slug = os.path.splitext(os.path.basename(excel_file_path))[0]
        self.grade_level = None
        self.pages = []
        self.output_dir = os.path.dirname(excel_file_path)
        self.read_excel_file()

    def read_excel_file(self):
        df = pd.read_excel(self.excel_file_path, header=None)

        page = {}
        images = {}
        for index, row in df.iterrows():
            key, value = str(row[0]).strip(), str(row[1]).strip()

            if key.lower().startswith('grade level'):
                self.grade_level = value
            elif key.lower().startswith('new readalong page'):
                if page:
                    if images:
                        page['images'] = images
                    self.pages.append(page)
                page = {"type": "readalong"}
                images = {}
            elif key.lower() == 'instructional image':
                images['instructionalImage'] = value
            elif key.lower() == 'instructional image alt tag':
                images['instructionalImageAltTag'] = value
            elif key.lower().startswith('instructions'):
                page['instructions'] = {
                    "text": value,
                    "showTextInstructions": value.lower() != "none",
                    "audio": os.path.join('./audio/', f"{self.slug}_page{len(self.pages) + 1}_instr.mp3")
                }
            elif key.lower().startswith('page text:'):
                page_text = value
                if page_text and page_text.lower() != 'nan':  
                    text_output_dir = os.path.join(self.output_dir, 'tmp', 'text')
                    os.makedirs(text_output_dir, exist_ok=True)
                    text_file_path = os.path.join(text_output_dir, f'{self.slug}_page{len(self.pages) + 1}_content.txt')
                    with open(text_file_path, 'w') as text_file:
                        text_file.write(page_text)
                    page["audio"] = os.path.join('./audio/', f"{self.slug}_page{len(self.pages) + 1}_content.mp3")
                else:
                    print(f"Warning: Page {len(self.pages) + 1} has no text.")
                    
        if page:
            if images:
                page['images'] = images
            self.pages.append(page)

    def to_dict(self):
        return {
            "slug": self.slug,
            "gradeLevel": self.grade_level,
            "pages": self.pages
        }

    def save_as_json(self):
        data = self.to_dict()
        json_file_path = os.path.join(self.output_dir, f'{self.slug}.json')
        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=4)
