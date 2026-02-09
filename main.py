import sys
import json
from pathlib import Path


def normalize(text):
    words = text.split()
    words = [word.strip('.,!?¿;"\'()[]') for word in words]
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
                "most_frequent": [
                    {"word": word, "count": freq} 
                    for word, freq in most_frequent.items()
                ]
            }
            return result
    except FileNotFoundError:
        print(f"File '{path}' not found.")
        sys.exit(1)


def main(path, json_file=None):
    general_result = {
        "total_documents": 0,
        "total_words": 0,
        "most_frequent": [
            {"word": "", "count": 0}
        ]
        }
    word_frequency = [
            {"word": "", "count": 0}
        ]
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
            for local_word_info in local_result["most_frequent"]:
                local_word = local_word_info["word"]
                local_count = local_word_info["count"]
                found = False
                for word_frequency_info in word_frequency:
                    if word_frequency_info["word"] == local_word:
                        word_frequency_info["count"] += local_count
                        found = True
                        break
                if not found:
                    word_frequency.append({
                        "word": local_word,
                        "count": local_count
                    })
    word_frequency = sorted(word_frequency, key=lambda x: x["count"], reverse=True)
    general_result["most_frequent"] = [
        {"word": word_info["word"], "count": word_info["count"]}
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
        print("Words in text: " + str(general_result["total_words"]))
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