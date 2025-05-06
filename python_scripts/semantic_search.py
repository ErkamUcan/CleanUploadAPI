import sys
import os
from sentence_transformers import SentenceTransformer, util

def load_chunks(video_id):
    chunks_folder = f"Chunks"
    chunks = []
    chunk_paths = []
    for filename in os.listdir(chunks_folder):
        if filename.startswith(video_id) and filename.endswith(".txt"):
            path = os.path.join(chunks_folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                chunks.append(f.read())
                chunk_paths.append(path)
    return chunks, chunk_paths

def main():
    if len(sys.argv) < 3:
        print(" Kullanım: python semantic_search.py \"SORU\" video_id")
        sys.exit()

    question = sys.argv[1]
    video_id = sys.argv[2]

    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    chunks, paths = load_chunks(video_id)

    if not chunks:
        print(" Chunk bulunamadı.")
        sys.exit()

    question_embedding = model.encode(question, convert_to_tensor=True)
    chunk_embeddings = model.encode(chunks, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(question_embedding, chunk_embeddings)[0]
    best_idx = similarities.argmax().item()

    best_chunk_path = paths[best_idx]
    print(best_chunk_path)  # 💡 Sadece path'i stdout'a yazıyoruz

if __name__ == "__main__":
    main()
