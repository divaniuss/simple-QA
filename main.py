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
collection = db['agent']


def AddQue(que):
    print("Ya ne znay, how to ansv?")
    ans = input("Add ansver: ")

    while True:
        try:
            rate = int(input("rate: "))
            break
        except ValueError:
            print("error. need int")

    doc = {
        "question": que,
        "answers": [{"text": ans, "rating": rate}]
    }
    collection.insert_one(doc)
    print("added")


def IsQuestion(que):
    found = collection.find_one({"question": que})

    if found:
        answers = found['answers']
        answers.sort(key=lambda x: x['rating'], reverse=True)
        best = answers[0]

        print(f"{best['text']}")

        print("1 - new rait 2 - new ansv else - next")
        choice = input("choice: ")

        if choice == "1":

            while True:
                try:
                    new_rating = int(input("add new rait: "))
                    break
                except ValueError:
                    print("error. need int")

            collection.update_one(
                {"_id": found["_id"], "answers.text": best["text"]},
                {"$set": {"answers.$.rating": new_rating}}
            )
            print(f"Added")

        elif choice == "2":
            new_ans = input("new ansver: ")

            while True:
                try:
                    new_rate = int(input("add rate: "))
                    break
                except ValueError:
                    print("error. need int")

            collection.update_one(
                {"_id": found["_id"]},
                {"$push": {"answers": {"text": new_ans, "rating": new_rate}}}
            )
            print("added")

    else:
        AddQue(que)

def CleanSort(que):
    symbols = "?!.,;:-()"
    for char in symbols:
        que = que.replace(char, "")
    words = que.split()
    words.sort()
    return " ".join(words)

while True:
    que = input("ask: ").strip().lower()
    clean_que = CleanSort(que)

    if que == "q":
        print("bye")
        break

    if que:
        IsQuestion(clean_que)