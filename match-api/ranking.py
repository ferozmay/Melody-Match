from utils.text_processing import process_text
import math


def tfidf(query: str, index, collection_size: int):
        # for each query term, calculate the weight of the term in each document
        # weight_t,d = (1 + log _10 tf (t,d) * log _10 (N/df(t))
        # tf(t,d) = frequency of term t in document d
        # df(t) = number of documents containing term t
        # N = total number of documents in the collection

        terms = process_text(query).split()
        term_dfs = {term: index[term]['Track']['Name']['doc_freq'] for term in terms if term in index}

        # for each doc, calculate the retrieval score
        # (the sum of the weights of the terms that appear in both the query and the document)

        retrieval_scores = {}
        
        # get docs to consider (any doc that contains at least one of the query terms)
        doc_ids = set()
        for term in terms:
            if term in index:
                doc_ids.update(index[term]['Track']['Name']['doc_ids'].keys())

        # for each doc, calculate the retrieval score
        for doc_id in doc_ids:
            if doc_id not in retrieval_scores:
                retrieval_scores[doc_id] = 0
            for term in terms:
                weight = 0
                if term in index and doc_id in index[term]['Track']['Name']['doc_ids']:
                    tf = len(index[term]['Track']['Name']['doc_ids'][doc_id])  # no. of listed appearances of term in doc = freq. in doc
                    df = term_dfs[term]

                    # skip if tf or df are zero to prevent math errors
                    if tf == 0 or df == 0:
                        continue

                    # calculate the tfidf weight
                    weight = (1 + math.log10(tf)) * math.log10(collection_size / df)
                    retrieval_scores[doc_id] += weight
        
        return retrieval_scores


# this is just something I was halfway through so can ignore
# def search_bm25rank(self, query: str, collection_size: int, hyperparams: dict):
#     query_tokens = process_text(query).split()
# 
#         # multiple search terms
#         doc_ids = set()
#         for term in query_tokens:
#             if term in self.inverted_index:
#                 doc_ids.update(self.inverted_index[term]['docs'].keys())



#         # for each doc, calculate the retrieval score
#         # (the sum of the weights of the terms that appear in both the query and the document)

#         retrieval_scores = {}
        


#         # for each doc, calculate the retrieval score
#         for doc_id in doc_ids:
#             doc_bm25 = 0
#             for term in query_tokens:
#                 term_bm25 = calculate_bm25(term, doc_id, collection_size, hyperparams)
#                 doc_bm25 += term_bm25
#             retrieval_scores[doc_id] = doc_bm25
#         return retrieval_scores
            
#     def calculate_bm25(self, term, doc_id, collection_size, hyperparams):
#         # calculate the BM25 score for a term in a document with hyperparameters k, b
#         # BM25(t,d) = IDF(t) * (tf(t,d) * (k + 1)) / (tf(t,d) + k * (1 - b + b * (doclength / avgdoclength)))
#         # IDF(t) = log((N - df(t) + 0.5) / (df(t) + 0.5))
#         # tf(t,d) = frequency of term t in document d
#         # df(t) = number of docs containing term t
#         # N = total number of docs in collection

#         k = hyperparams['k']
#         b = hyperparams['b']

#         # we need to get the length of the document (after pre-processing) and the average length of all documents
        

#         idft = math.log((collection_size - self.inverted_index[term]['doc_freq'] + 0.5) / (self.inverted_index[term]['doc_freq'] + 0.5))
#         denom = len(self.inverted_index[term]['docs'][doc_id]) * (k + 1)
#         numer = len(self.inverted_index[term]['docs'][doc_id]) + k * (1 - b + b * (len(self.inverted_index[term]['docs'][doc_id]) / self.avg_title_length))
              
        
#             weight = 0
#                 if term in self.inverted_index and doc_id in self.inverted_index[term]['docs']:
#                     tf = len(self.inverted_index[term]['docs'][doc_id]) # no. of listed appearances of term in doc = freq. in doc
#                     df = self.inverted_index[term]['doc_freq']
#                     weight = (1 + math.log10(tf)) * math.log10(collection_size / df)
#                     retrieval_scores[doc_id] += weight
