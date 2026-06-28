import chromadb

client = chromadb.PersistentClient(
    path="./vector_db"
)

collection = client.get_collection(
    "hsbc_kpis"
)

print(
    "Vector Count:",
    collection.count()
)   