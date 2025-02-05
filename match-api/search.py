from utils.text_processing import process_text

def simple_search(query: str, index):

        query_tokens = process_text(query).split()

        term_doc_ids = []

        if len(query_tokens) == 1:
            term = query_tokens[0]
            if term in index:
                term_doc_ids.append(set(index[term]['docs'].keys()))
                docs = index[term]['docs'].keys()
                return docs

        # multiple search terms
        for term in query_tokens:
            if term in index:
                term_doc_ids.append(set(index[term]['docs'].keys()))
        
        if not term_doc_ids:
            return []
                
        common_doc_ids = set.intersection(*term_doc_ids)

        results = list(common_doc_ids)
        
        return results
