from .lexer import new_lexer


def run(input_file_address: str) -> str:
    result = ''

    input_file = open(input_file_address)
    input_content = input_file.read()

    return new_lexer(input_content)
    # for token in input_content.splitlines():
    #     result += token
    #     result += "\n"
    # return result
