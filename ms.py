import json

with open("data/ms.md", "r") as f:
    lines = f.readlines()
    qas = []
    seen = set()  # 用于记录已处理的问答对
    with open("data/xl.json", "r") as xlf:
        xls = json.load(xlf)
        for qa in xls:
            question = qa["question"]
            answer = qa["answer"]
            seen.add((question, answer))
    for line in lines:
        line = line.strip()
        segs = line.split("-----")
        question = segs[0].split(" ")
        qa = {
                "question": "".join(question[1:]),
                "answer": "".join(segs[1:]),
            }
        # 检查是否重复
        if (qa["question"], qa["answer"]) not in seen:
            qas.append(qa)
            seen.add((qa["question"], qa["answer"]))
            print(qa)

    with open("data/ms.json", "w") as f:
        json.dump(qas, f, ensure_ascii=False, indent=4)
        print("ms.json created.")
