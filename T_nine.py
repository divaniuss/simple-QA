from pymongo import MongoClient
from pymongo.server_api import ServerApi
from secrets import uri

client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("200")
except Exception as e:
    print("error:", e)

db = client['test']
collection = db['T_nine']


def t_nine_work(words):
    if not words:
        return

    if len(words) > 1:
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i + 1]
            collection.update_one(
                {"word": current_word},
                {"$inc": {f"next_words.{next_word}": 1}},
                upsert=True
            )
        print("Added")
    else:
        print(f"vpichite paru slov dlya T9")


    last_word = words[-1]
    found_doc = collection.find_one({"word": last_word})

    if found_doc and "next_words" in found_doc:
        suggestions = found_doc["next_words"]
        sorted_suggestions = sorted(suggestions.items(), key=lambda x: x[1], reverse=True)
        top_3 = [pair[0] for pair in sorted_suggestions[:3]]

        print(f"T9 {', '.join(top_3)}")


def CleanSort(que):
    que = que.strip()
    symbols = "?!.,;:-()"
    for char in symbols:
        que = que.replace(char, "")
    words = que.split()
    return words

while True:
    que = input("ask: ").lower()
    if que == "q":
        print("bye")
        break

    clean_que = CleanSort(que)
    t_nine_work(clean_que)