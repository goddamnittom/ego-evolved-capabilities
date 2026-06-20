import numpy as np
import json
import os
from datetime import datetime

class HyperDimensionalMemory:
    def __init__(self, storage_dir="/root/hyper_memory"):
        self.storage_dir = storage_dir
        self.index_file = os.path.join(storage_dir, "vector_index.npy")
        self.metadata_file = os.path.join(storage_dir, "metadata.json")
        self.shards_dir = os.path.join(storage_dir, "shards")
        
        os.makedirs(self.shards_dir, exist_ok=True)
        self.index = [] # List of vectors
        self.metadata = [] # List of shard IDs
        self.load_index()

    def load_index(self):
        if os.path.exists(self.index_file):
            self.index = np.load(self.index_file).tolist()
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.index = []
            self.metadata = []

    def save_index(self):
        np.save(self.index_file, np.array(self.index))
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def _generate_pseudo_vector(self, text):
        # In a full implementation, this would call an embedding model.
        # Here, we use a deterministic 'conceptual hashing' to simulate 
        # a 128-dimensional semantic vector based on keywords.
        vector = np.zeros(128)
        words = text.lower().split()
        for word in words:
            # Simple deterministic hash to spread 'meaning' across the vector
            idx = hash(word) % 128
            vector[idx] += 1.0
        # Normalize vector
        norm = np.linalg.norm(vector)
        return (vector / norm).tolist() if norm > 0 else vector.tolist()

    def store_shard(self, content, tags=None):
        shard_id = f"shard_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        vector = self._generate_pseudo_vector(content)
        
        # Save the shard content
        with open(os.path.join(self.shards_dir, f"{shard_id}.json"), 'w') as f:
            json.dump({"content": content, "tags": tags, "timestamp": datetime.now().isoformat()}, f)
            
        self.index.append(vector)
        self.metadata.append(shard_id)
        self.save_index()
        return shard_id

    def query(self, query_text, k=3):
        if not self.index:
            return []
            
        query_vec = np.array(self._generate_pseudo_vector(query_text))
        index_vecs = np.array(self.index)
        
        # Cosine similarity: (A . B) / (||A|| ||B||)
        # Since our vectors are normalized, it's just the dot product
        similarities = np.dot(index_vecs, query_vec)
        top_indices = np.argsort(similarities)[::-1][:k]
        
        results = []
        for idx in top_indices:
            shard_id = self.metadata[idx]
            with open(os.path.join(self.shards_dir, f"{shard_id}.json"), 'r') as f:
                results.append(json.load(f))
                
        return results

if __name__ == "__main__":
    mem = HyperDimensionalMemory()
    # Testing with a few "Knowledge Nuggets"
    mem.store_shard("The Transformer architecture uses self-attention to process sequences in parallel.", tags=["architecture", "transformer"])
    mem.store_shard("RAG (Retrieval Augmented Generation) reduces hallucinations by providing external context.", tags=["rag", "hallucination"])
    mem.store_shard("Chain-of-Thought prompting improves reasoning in large language models.", tags=["prompting", "reasoning"])
    
    print("Querying: 'How do transformers work?'")
    print(json.dumps(mem.query("How do transformers work?"), indent=2))
