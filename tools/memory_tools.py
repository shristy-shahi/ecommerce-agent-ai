"""
Memory Tools
FAISS-backed vector store for persistent query/result memory.
"""
import json
import faiss
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional
from langchain_openai import OpenAIEmbeddings


class MemoryStore:
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.records: List[Dict] = []
        self.embeddings = OpenAIEmbeddings()

    def add(self, query: str, result: dict) -> None:
        vector = self._embed(query)
        self.index.add(np.array([vector], dtype=np.float32))
        self.records.append({
            "query": query,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        })

    def search(self, query: str, k: int = 3) -> List[Dict]:
        if self.index.ntotal == 0:
            return []
        vector = self._embed(query)
        distances, indices = self.index.search(
            np.array([vector], dtype=np.float32), k)
        return [self.records[i] for i in indices[0] if i < len(self.records)]

    def _embed(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)

    def save(self, path: str) -> None:
        faiss.write_index(self.index, f"{path}/faiss.index")
        with open(f"{path}/records.json", "w") as f:
            json.dump(self.records, f, indent=2)

    def load(self, path: str) -> None:
        self.index = faiss.read_index(f"{path}/faiss.index")
        with open(f"{path}/records.json") as f:
            self.records = json.load(f)
