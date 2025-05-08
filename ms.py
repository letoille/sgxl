import json

with open("data/ms.md", "r") as f:
    lines = f.readlines()
    qas = []
    for line in lines:
        line = line.strip()
        segs = line.split("-----")
        question = segs[0].split(" ")
        qa = {
                "question": "".join(question[1:]),
                "answer": "".join(segs[1:]),
            }
        qas.append(qa)
        print(qa)
    with open("data/ms.json", "w") as f:
        json.dump(qas, f, ensure_ascii=False, indent=4)
        print("ms.json created.")
