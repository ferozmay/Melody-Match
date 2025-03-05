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



def evaluate_postfix(postfix_tokens, search_index):
    stack = []
    print(postfix_tokens)
    for token in postfix_tokens:
        if token.isalnum() and token not in ["AND", "OR", "NOT"]:
            docs = search_index.lookup(token)
            # print(f"Lookup for '{token}': {docs}")
            stack.append(docs)
            # print(f"Stack: {stack}")
        elif token == "AND":
            right = stack.pop()
            left = stack.pop()
            # print(f"AND operation: {left} & {right}")
            result = left & right
            # print(f"Result: {result}")
            stack.append(result)
            # print(f"Stack: {stack}")
        elif token == "NOT":
            operand = stack.pop()
            # print(f"NOT operation: {operand}")
            # Assuming a universal document set (optional, depends on implementation)
            all_docs = set.union(*search_index.index.values()) if search_index.index else set()
            # print(f"all_docs: {all_docs}")
            stack.append(all_docs - operand)
        elif token == "OR":
            right = stack.pop()
            left = stack.pop()
            stack.append(left | right)

    return stack[0] if stack else set()


def boolean_tokenize(query):
    return re.findall(r'\(|\)|\w+|AND|OR|NOT', query)


def unit_test_infix_to_postfix():
    query = "NOT apple AND banana OR cherry AND (date OR NOT fig)"
    tokens = boolean_tokenize(query)
    postfix = infix_to_postfix(tokens)
    expected_postfix = ["apple", "NOT", "banana", "AND", "cherry", "date", "fig", "NOT", "OR", "AND", "OR"]
    assert postfix == expected_postfix, f"Expected {expected_postfix}, but got {postfix}"
    print("Infix2Postfix test passed!")


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
    # print("Boolean search test passed!")


def generate_sample_index():
    search_index = SearchIndex()
    search_index.add_document(1, ["apple", "banana", "cherry"])
    search_index.add_document(2, ["apple", "cherry", "date"])
    search_index.add_document(3, ["cherry", "date", "fig"])
    search_index.add_document(4, ["date", "fig", "apple"])
    search_index.add_document(5, ["fig", "apple", "banana"])
    search_index.add_document(6, ["apple", "banana", "cherry"])
    search_index.add_document(7, ["fig", "apple", "banana"])
    return search_index


class SearchIndex:
    def __init__(self):
        self.index = {}

    def add_document(self, doc_id, terms):
        for term in terms:
            if term not in self.index:
                self.index[term] = set()
            self.index[term].add(doc_id)

    def lookup(self, term):
        return self.index.get(term, set())


if __name__ == "__main__":
    unit_test_infix_to_postfix()
    unit_test_boolean_search()
