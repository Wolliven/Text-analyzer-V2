import sys
import json
from pathlib import Path


def normalize(text):
    words = text.split()
    words = [word.strip('.,!?¿;"\'()[]:-…') for word in words]
    filtered_words = [word for word in words if word]
    return filtered_words

def count_words(words):
    return len(words)

def most_frequent_words(words):
    frequency = {}
    for word in words:
        word = word.lower()
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency

def analyze_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = normalize(f.read())
            counted_words = count_words(content)
            most_frequent = most_frequent_words(content)
            result ={
                "total_words": counted_words,
                "most_frequent": most_frequent
            }
            return result
    except FileNotFoundError:
        print(f"File '{path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while processing the file '{path}': {e}")
        return None


def main(path, json_file=None):
    general_result = {
        "total_documents": 0,
        "total_words": 0,
        "most_frequent": []
        }
    word_frequency = {}
    
    p = Path(path)
    if not p.exists():
        print(f"The folder '{path}' does not exist.")
        sys.exit(1)
    if not p.is_dir():
        print(f"'{path}' is not a folder.")
        sys.exit(1)

    for file_path in Path(path).iterdir():
        if file_path.is_file():
            if not file_path.suffix == '.txt':
                continue
            general_result["total_documents"] += 1
            local_result = analyze_file(file_path)
            if not local_result or local_result["total_words"] == 0:
                print(f"The file '{file_path}' does not contain any valid words.")
                continue
            general_result["total_words"] += local_result["total_words"]
            for local_word, local_count in local_result["most_frequent"].items():
                word_frequency[local_word] = word_frequency.get(local_word, 0) + local_count

    word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
    general_result["most_frequent"] = [
        {"word": word_info[0], "count": word_info[1]}
        for word_info in word_frequency[:10]
    ]

    #Create the Json file based on the name provided by the user or default to result.json
    if json_file:
        if not json_file.endswith('.json'):
            json_file += '.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(general_result, f, indent=4, ensure_ascii=False)
    else:
        print(f"Files analyzed: {general_result['total_documents']}")
        print("Total words: " + str(general_result["total_words"]))
        print("Most frequent words: ")
        for word_info in general_result["most_frequent"]:
            print(f"'{word_info['word']}' appears {word_info['count']} times")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        folder = sys.argv[1]
        main(folder)
    elif len(sys.argv) == 3:
        folder = sys.argv[1]
        json_file = sys.argv[2]
        main(folder, json_file)
    else:
        print("Program usage: python main.py [folder name] [JSON file name (optional)]")
        sys.exit(1)