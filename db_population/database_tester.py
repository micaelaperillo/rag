from database.ChromaManager import ChromaManager

def test_database():
    chroma_manager = ChromaManager()
    chroma_manager.get_collection("videos")
    query = input("Enter your search query: ")
    print(f"\nSearching for '{query}'...")
    results = chroma_manager.search_video_chunks(query)
    print(f"\nFound {len(results)} results:\n")
    for i, result in enumerate(results['documents'][0], 1):
        print(f"Result {i}:")
        print("=" * 40)
        print(result)
        print()

if __name__ == "__main__":
    test_database()