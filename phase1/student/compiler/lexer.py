from lark import Lark
from lark import Transformer
import re


# you can write here and import this file in main!

def replace_line(define_map, line):
    line = re.split('( |"|\[|]|\(|\))', line)
    for i in range(len(line)):
        if line[i] in define_map:
            line[i] = define_map[line[i]]
    answer = ""
    for i in line:
        answer += i
    return answer


def replace_defines(input):
    input_array = input.split("\n")
    define_map = {}
    answer = ""
    for line in input_array:
        line = replace_line(define_map, line)
        split_form = line.split()
        if len(split_form) >= 3 and split_form[0] == 'define':
            define_map[split_form[1]] = " ".join(split_form[2:])
        else:
            answer += line + "\n"
    return answer


rules = """
    start : (ID | OPERATOR_PUNC | INT_LIT | DOUBLE_LIT | COMMENT | STRING_LIT )*
                
    ID: /[a-zA-Z][a-zA-Z0-9_]*/ | /__func__[a-zA-Z0-9_]*/ | /__line__[a-zA-Z0-9_]*/ 
    OPERATOR_PUNC: "+" | "-" | "*" | "/" | "%" | "<" | "<=" | ">" | ">=" | "=" 
                    | "+=" | "-=" | "-+" | "*=" | "/=" | "==" | "!=" | "&&" |  "||" 
                    | "!" | ";" | "," | "." | "[" | "]" | "(" | ")" | "{" | "}"  
    MIDDLE_STRING_CHAR : /[^"]/
    STRING_LIT : /\\"[^"]*\\"/ 
    INT_LIT : /0[Xx][0-9a-fA-F]+/ | /[0-9]+/
    DOUBLE_LIT : /[0-9]+\\.[0-9]*/ | /[0-9]+\\.[0-9]*[Ee][+-]?[0-9]+/
    COMMENT.1 : "//"/[^\\n]*/"\\n" | "/*" /.*/ "*/" | "/*" /.*/ "\\n" | /\\/\\*[(\\s\\S)^(\\/)]*\\*\\//
    %import common.WS -> WS
    %ignore WS
    %ignore COMMENT
"""
all_tokens = []

keywords = ["__func__", "__line__", "bool", "break", "btoi",
            "class", "continue", "double", "dtoi", "else", "for", "if",
            "import", "int", "itob", "itod", "new", "NewArray", "null",
            "Print", "private", "public", "ReadInteger", "ReadLine",
            "return", "string", "this", "void", "while"]

bools = ["true", "false"]


class T(Transformer):
    def ID(self, token):
        if token in keywords:
            all_tokens.append(token)
            return token
        elif token in bools:
            all_tokens.append(("T_BOOLEANLITERAL " + token))
            return "T_BOOLEANLITERAL " + token
        else:
            if token[0] == '_':
                # all_tokens.append(("T_ID " + token))
                raise NotImplemented
            all_tokens.append(("T_ID " + token))
            return "T_ID " + token

    def INT_LIT(self, token):
        all_tokens.append(("T_INTLITERAL " + token))
        return "T_INTLITERAL " + token

    def DOUBLE_LIT(self, token):
        all_tokens.append(("T_DOUBLELITERAL " + token))
        return "T_DOUBLELITERAL " + token

    def STRING_LIT(self, token):
        append_to_prev = False
        if len(token) >= 2 and token[len(token) - 2] == '\\':
            token = token[:-1]
            append_to_prev = True

        if hasattr(self, "append_to_prev") and self.append_to_prev:
            all_tokens[len(all_tokens) - 1] += token
        else:
            all_tokens.append(("T_STRINGLITERAL " + token))

        self.append_to_prev = append_to_prev

        return "T_STRINGLITERAL " + token

    def OPERATOR_PUNC(self, token):
        all_tokens.append(token)
        return token

    def __default_token__(self, token):
        all_tokens.append(token)
        return super().__default_token__(token)


def new_lexer(string):
    string = replace_defines(string + ' ')
    all_tokens.clear()
    string = string.replace('\\"', '\\""')
    parser = Lark(rules, parser='lalr', transformer=T())
    parser.parse(string + ' ')
    return '\n'.join(all_tokens) + "\n"
