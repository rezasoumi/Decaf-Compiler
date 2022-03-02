from .lexer import new_lexer


def run(input_file_address: str) -> str:
    result = ''

    input_file =  open(input_file_address)
    input_content = input_file.read()

    # just kidding, it's not that simple
    # you should actually scan the file
    # this is just example
    for token in input_content.splitlines():
        result += token
        result += "\n"

    return result
