import os, faiss, traceback, json

from numpy import ndarray
from faiss import IndexFlatIP
from sentence_transformers import SentenceTransformer

class RagClass():
    def __init__(self):
        with open("./questao_3/contents.json", "r", encoding = "utf-8") as file:
            self.documents: list = json.load(file)

            if not self.documents:
                raise Exception("O arquivo JSON não possui documentos.")
        
        self.model: SentenceTransformer = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        
        self.index_path: str = "./questao_3/documents.faiss"
        self.index: IndexFlatIP = self.load_or_create_index()
    
    def load_or_create_index(self) -> IndexFlatIP:
        """Gera os embeddings, armazena no FAISS e cria o índice se existir ou devolve um já existente."""
        
        try:
            if os.path.exists(self.index_path):
                return faiss.read_index(self.index_path)
            else:
                embeddings: ndarray = self.model.encode(self.documents, convert_to_numpy = True, normalize_embeddings = True)
                
                faiss.normalize_L2(embeddings)
                
                dimensions = embeddings.shape[1]
                
                index: IndexFlatIP = faiss.IndexFlatIP(dimensions)
                
                index.add(embeddings)
                
                faiss.write_index(index, self.index_path)

                return index
        except Exception as ex:
            raise
    
    def search_docs(self, query: str, top_k: int) -> list:
        """Retorna os documentos semanticamente mais semelhantes."""

        try:
            query_embedding: ndarray = self.model.encode([query], convert_to_numpy = True, normalize_embeddings = True).astype("float32")

            top_k: int = min(top_k, len(self.documents))
            
            similarities, positions = self.index.search(query_embedding, top_k)
        
            return [
                {
                    "similarity": float(similarity),
                    "doc": self.documents[position]
                }
                for similarity, position in zip(similarities[0], positions[0])
            ]
        except Exception as ex:
            raise

if __name__ == "__main__":
    try:
        rag_class: RagClass = RagClass()

        query: str = "Quais ferramentas podem ser usadas para busca vetorial?"
        top_k: int = 3
        
        results: list = rag_class.search_docs(query, top_k)
        
        print("-" * 100)
        print(f"CONSULTA: {query}")
        print("-" * 100)
        print("")

        for result in results:
            print(f"SIMILARIDADE: {result['similarity']:.4f}")
            print("")
            print(result['doc'])
            print("")
            print("-" * 100)
            print("")
    except Exception as ex:
        traceback.print_exc()
        
        exit(0)
