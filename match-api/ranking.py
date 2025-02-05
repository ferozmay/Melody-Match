from utils.text_processing import process_text
import math


def tfidf(query: str, index, collection_size: int):
        # for each query term, calculate the weight of the term in each document
        # weight_t,d = (1 + log _10 tf (t,d) * log _10 (N/df(t))
        # tf(t,d) = frequency of term t in document d
        # df(t) = number of documents containing term t
        # N = total number of documents in the collection

        terms = process_text(query).split()
        term_dfs = {term: index[term]['doc_freq'] for term in terms}

        # for each doc, calculate the retrieval score
        # (the sum of the weights of the terms that appear in both the query and the document)

        retrieval_scores = {}
        
        # get docs to consider (any doc that contains at least one of the query terms)
        doc_ids = set()
        for term in terms:
            if term in index:
                doc_ids.update(index[term]['docs'].keys())

        # for each doc, calculate the retrieval score
        for doc_id in doc_ids:
            if doc_id not in retrieval_scores:
                retrieval_scores[doc_id] = 0
            for term in terms:
                weight = 0
                if term in index and doc_id in index[term]['docs']:
                    tf = len(index[term]['docs'][doc_id])  # no. of listed appearances of term in doc = freq. in doc
                    df = term_dfs[term]

                    # skip if tf or df are zero to prevent math errors
                    if tf == 0 or df == 0:
                        continue

                    # calculate the tfidf weight
                    weight = (1 + math.log10(tf)) * math.log10(collection_size / df)
                    retrieval_scores[doc_id] += weight
        
        return retrieval_scores
    