import json
import string

def format_json_function(input_json_file, input_txt_file, output_file):
    print(f'*** formatting {input_json_file} ***')
    with open(input_json_file, 'r') as f:
        data = json.load(f)

    with open(input_txt_file, 'r') as f:
        transcript = f.read()
        transcript_lines = transcript.split("\n")

    text = [{"begin": "0.000", "children": [], "end": "0.000", "id": "HEAD", "language": None, "lines": []}]

    word_idx = 0

    for line_idx, line in enumerate(transcript_lines):
        words_in_line = line.split()
        for transcript_word in words_in_line:
            if word_idx >= len(data["words"]):
                print(f"Ran out of words in JSON data on line {line_idx + 1} for {input_json_file}.")
                break

            # Remove punctuation for matching
            sanitized_transcript_word = transcript_word.strip(string.punctuation).lower()
            json_word = data["words"][word_idx]["word"].lower() if "word" in data["words"][word_idx] else None
            
            if sanitized_transcript_word != json_word:
                print(f"Warning: Skipped '{transcript_word}' on line {line_idx + 1} for {input_json_file}.")
                continue

            json_word_has_start = "start" in data["words"][word_idx]
            next_word_has_start = word_idx + 1 < len(data["words"]) and "start" in data["words"][word_idx + 1]
            
            item = {
                "begin": "{:.3f}".format(data["words"][word_idx]["start"]) if json_word_has_start else "N/A",
                "children": [],
                "end": "{:.3f}".format(data["words"][word_idx + 1]["start"]) if next_word_has_start else "{:.3f}".format(data["words"][word_idx]["end"]) if json_word_has_start else "N/A",
                "id": f"f{word_idx:06}",
                "language": "eng",
                "lines": [transcript_word]
            }

            text.append(item)
            word_idx += 1

        if line_idx < len(transcript_lines) - 1:
            text.append({"lines": [], "tags": "lineBreak"})

    text.append({
        "begin": "{:.3f}".format(data["words"][-1]["end"]) if len(data["words"]) > 0 and "end" in data["words"][-1] else "N/A",
        "children": [],
        "end": "{:.3f}".format(data["words"][-1]["end"]) if len(data["words"]) > 0 and "end" in data["words"][-1] else "N/A",
        "id": "TAIL",
        "language": None,
        "lines": []
    })

    with open(output_file, 'w') as f:
        json.dump({"text": text}, f, indent=4)
