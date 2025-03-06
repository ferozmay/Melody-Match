import re


def infix_to_postfix(tokens):
    precedence = {"NOT": 3, "AND": 2, "OR": 1}
    right_associative = {"NOT"}  # Only NOT is right-associative
    output = []
    stack = []
    for token in tokens:
        if token.isalnum() and token not in precedence:
            output.append(token)
        elif token == "NOT":
            stack.append(token)
        elif token in ("AND", "OR"):
            while stack and stack[-1] != "(" and precedence[stack[-1]] >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if stack and stack[-1] == "(":
                stack.pop()  # Remove '('
    while stack:
        output.append(stack.pop())
    return output



def evaluate_postfix(
        postfix_tokens, 
        search_index, 
        access_function=lambda term, index: index.get(term, set())
    ):
    """
    Evaluate the boolean expression in postfix notation.
    :param postfix_tokens: A list of tokens in postfix notation.
    :param search_index: A SearchIndex object.
    :return: A set of document IDs that satisfy the boolean expression.
    """
    # compute universal set once
    all_values = [access_function(term, search_index) for term in search_index.keys()]
    all_docs = set.union(*all_values) if search_index else set()
    # 
    stack = []
    for token in postfix_tokens:
        if token.isalnum() and token not in ["AND", "OR", "NOT"]:
            print("retrieve")
            docs = set(access_function(token, search_index))
            # print(f"Lookup for '{token}': {docs}")
            stack.append(docs)
            # print(f"Stack: {stack}")
        elif token == "AND":
            print("AND")
            right = stack.pop()
            left = stack.pop()
            # print(f"AND operation: {left} & {right}")
            result = left & right
            # print(f"Result: {result}")
            stack.append(result)
            # print(f"Stack: {stack}")
        elif token == "NOT":
            print("NOT")
            operand = stack.pop()
            # print(f"NOT operation: {operand}")
            # apply not to previous operand
            # if stack:
            #     previous_operand = stack[-1] if stack else set()
            #     result = previous_operand.difference(operand)
            # else:
            result = all_docs - operand
            # print(f"all_docs: {all_docs}")
            stack.append(result)
            # print(f"Stack: {stack}")
        elif token == "OR":
            print("OR")
            right = stack.pop()
            left = stack.pop()
            # print(f"OR operation: {left} | {right}")
            stack.append(left | right)
            # print(f"Stack: {stack}")
    # print(f"Final stack: {stack}")
    return set(stack[0]) if stack else set()


def boolean_tokenize(query):
    # First, extract all tokens using regex
    raw_tokens = re.findall(r'\(|\)|\w+|AND|OR|NOT', query)
    # Now insert AND between adjacent regular terms
    result = []
    for i, token in enumerate(raw_tokens):
        result.append(token)
        # Check if we need to insert an AND
        if i < len(raw_tokens) - 1:
            current = token
            next_token = raw_tokens[i + 1]
            # Insert AND if:
            # 1. Current token is a term or closing bracket
            # 2. Next token is a term or opening bracket
            # 3. Neither is an operator
            if (current not in ["AND", "OR", "NOT", "("]) and \
               (next_token not in ["AND", "OR", "NOT", ")", "("]) and \
               (current != ")" or next_token != "("):
                result.append("AND")
    return result


def unit_test_infix_to_postfix():
    query = "NOT apple AND banana OR cherry AND (date OR NOT fig)"
    tokens = boolean_tokenize(query)
    postfix = infix_to_postfix(tokens)
    expected_postfix = ["apple", "NOT", "banana", "AND", "cherry", "date", "fig", "NOT", "OR", "AND", "OR"]
    assert postfix == expected_postfix, f"Expected {expected_postfix}, but got {postfix}"
    print("Infix2Postfix test passed!")


def unit_test_not_operator():
    #     apple     AND NOT    fig
    # {1,2,4,5,6,7} AND NOT {3,4,5,7}
    # {1,2,4,5,6,7} AND {1,2,6}
    #           {1,2,6}
    query = "apple AND NOT fig"
    tokens = boolean_tokenize(query)
    postfix = infix_to_postfix(tokens)
    search_index = generate_sample_index()
    result = evaluate_postfix(postfix, search_index)
    expected_result = {1, 2, 6}
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    print("NOT operator test passed!")


def unit_test_boolean_search():
    #   (  apple     AND  banana)   OR   (cherry  AND (date    OR NOT   fig))
    # ({1,2,4,5,6,7} AND {1,5,6,7}) OR ({1,2,3,6} AND ({2,3,4} OR NOT {3,4,5,7} ))
    #           {1,5,6,7}           OR  {1,2,3,6} AND ({2,3,4} OR {1,2,6})
    #           {1,5,6,7}           OR  {1,2,3,6} AND {1,2,3,4,6})
    #           {1,5,6,7}           OR  {1,2,3,6}
    #                         {1,2,3,5,6,7}
    query = "apple AND banana OR cherry AND (date OR NOT fig)"
    tokens = boolean_tokenize(query)
    postfix = infix_to_postfix(tokens)
    search_index = generate_sample_index()
    result = evaluate_postfix(postfix, search_index)
    expected_result = {1, 2, 3, 5, 6, 7}
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    print("Boolean search test passed!")


def generate_sample_index() -> dict:
    search_index = SearchIndex()
    search_index.add_document(1, ["apple", "banana", "cherry"])
    search_index.add_document(2, ["apple", "cherry", "date"])
    search_index.add_document(3, ["cherry", "date", "fig"])
    search_index.add_document(4, ["date", "fig", "apple"])
    search_index.add_document(5, ["fig", "apple", "banana"])
    search_index.add_document(6, ["apple", "banana", "cherry"])
    search_index.add_document(7, ["fig", "apple", "banana"])
    return search_index.index


class SearchIndex:
    def __init__(self):
        self.index = {}

    def add_document(self, doc_id, terms):
        for term in terms:
            if term not in self.index:
                self.index[term] = set()
            self.index[term].add(doc_id)


if __name__ == "__main__":
    unit_test_infix_to_postfix()
    unit_test_not_operator()
    # q = "green oranges OR (black 50 cent)"
    # t = boolean_tokenize(q)
    # print(t)
    unit_test_boolean_search()
