from app.services.vectorstore_service import get_vectorstore


def retrieve_documents(query, k=5):
    vectorstore = get_vectorstore()
    
    # Step 1: retrieve more candidates (increase recall)
    results = vectorstore.similarity_search(query, k=k)

    #step 2: heuristic scoring
    query_words = query.lower().split()
    stopwords =["the", "is", "at", "a", "an", "to", "for", "on", "in", "of", "and"]

    document_score =[]
    for doc in results:
        content = doc.page_content.lower()
        #count words in doc overlapping with query
        score = sum(1 for word in query_words if word in content and word not in stopwords)

        document_score.append((doc,score))
        # Step 3: sort by score (high → low)
        
    document_score.sort(key =lambda x: x[1], reverse=True)
    for i, (doc,score) in enumerate(document_score[:5],1):
        source = doc.metadata.get("source", "unknown")
        preview = doc.page_content[:100].replace("\n", " ")
        print(f"{i}. score = {score} | source = {source} | preview = {preview}")


    top_docs = [doc for doc, _ in document_score[:3]]
    
    return top_docs






 



    


