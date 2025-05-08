import logging
import json

from fastapi import FastAPI
from pydantic import BaseModel
import chromadb

app = FastAPI()
client = chromadb.PersistentClient(path="persist")
try:
    collection = client.get_collection("sgxl")
except Exception as e:
    collection = client.create_collection("sgxl")

def load_xl_data() -> list[dict]:
    qas = json.load(open("data/xl.json", "r"))
    documents = []
    for qa in qas:
        question = qa["question"]
        answer = qa["answer"]
        documents.append(
            {
                "question": question,
                "answer": answer,
            }
        )
    return documents

def load_to_chroma():
    logging.info("Loading data into ChromaDB...")
    docs = load_xl_data()
    id = 0
    for doc in docs:
        id += 1
        collection.add(
            documents=[doc["question"]],
            metadatas=[doc],
            ids=[str(id)],
        )
    logging.info("Data loaded into ChromaDB.")

class Question(BaseModel):
    question: str

@app.post('/xl/question')
def xl_question(question: Question):
    try:
        answer = collection.query(query_texts=[question.question], n_results=3)
        logging.info(answer)
        if not answer or not answer.get('metadatas') or len(answer.get('metadatas')) == 0:
            return {
                "error": "No answer found",
            }
        else:
            return answer.get('metadatas')[0]
    except Exception as e:
        return {
            "error": str(e),
        }


if __name__ == "__main__":
    import uvicorn
    import os

    project_path = os.path.abspath(os.path.dirname(__file__))
    logging.basicConfig(level=logging.INFO, filename=os.path.join(project_path, "logs/sgxl.log"), filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info("Starting sgxl server...")
    if collection.count() == 0:
        load_to_chroma()
    else:
        logging.info("ChromaDB already loaded, skipping load.")

    uvicorn.run(app, host="0.0.0.0", port=8080)
