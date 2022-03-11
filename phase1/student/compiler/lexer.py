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


all_keywords = ["__func__"  "__line__"
                "bool", "break", "btoi ", "class ", "continue",
                "double", "dtoi", "else", "for",
                "if", "import", "int", "itob",
                "itod", "new", "NewArray", "null", "Print", "private", "public",
                "ReadInteger", "ReadLine", "return", "string", "this", "void  ", "while",
                ]
rules = """
    start : (ID | OPERATOR_PUNC | KEYWORDS | BOOLEAN_LIT | INT_LIT | DOUBLE_LIT | COMMENT | STRING_LIT )*
    KEYWORDS.1: "__func__" | "__line__" 
                | /bool[\\s]/ | /break[\\s]/ | /btoi[\\s]/ | /class[\\s]/ | /continue[\\s]/ 
                | /double[\\s]/|  /dtoi[\\s]/|  /else[\\s]/|  /for[\\s]/|  /if[\\s]/ |  /import[\\s]/|  /int[\\s]/|  /itob[\\s]/ 
                | /itod[\\s]/ | /new[\\s]/|  /NewArray[\\s]/|  /null[\\s]/|  /Print[\\s]/|  /private[\\s]/|  /public[\\s]/ 
                | /ReadInteger[\\s]/|  /ReadLine[\\s]/|  /return[\\s]/|  /string[\\s]/|  /this[\\s\\S]/ |  /void[\\s]/ |  /while[\\s]/
                
    ID: /[a-zA-Z][a-zA-Z0-9_]*/
    OPERATOR_PUNC: "+" | "-" | "*" | "/" | "%" | "<" | "<=" | ">" | ">=" | "=" 
                    | "+=" | "-=" | "-+" | "*=" | "/=" | "==" | "!=" | "&&" |  "||" 
                    | "!" | ";" | "," | "." | "[" | "]" | "(" | ")" | "{" | "}"  
    MIDDLE_STRING_CHAR : /[^"]/
    STRING_LIT : "\\""/[^"]*/"\\""
    BOOLEAN_LIT.1: "true" | "false" 
    INT_LIT : /0[Xx][0-9a-fA-F]+/ | /[0-9]+/
    DOUBLE_LIT : /[0-9]+\\.[0-9]*/ | /[0-9]+\\.[0-9]*[Ee][+-]?[0-9]+/
    COMMENT.1 : "//"/[^\\n]*/"\\n" | "/*" /.*/ "*/" | "/*" /.*/ "\\n"
    %import common.WS -> WS
    %ignore WS
    %ignore COMMENT
"""
all_tokens = []


class T(Transformer):
    def ID(self, token):
        if token in all_keywords:
            token = token.rstrip()
            all_tokens.append(token)
            return token
        all_tokens.append(("T_ID " + token))
        return "T_ID " + token

    def BOOLEAN_LIT(self, token):
        all_tokens.append(("T_BOOLEANLITERAL " + token))
        return "T_BOOLEANLITERAL " + token

    def INT_LIT(self, token):
        all_tokens.append(("T_INTLITERAL " + token))
        return "T_INTLITERAL " + token

    def DOUBLE_LIT(self, token):
        all_tokens.append(("T_DOUBLELITERAL " + token))
        return "T_DOUBLELITERAL " + token

    def STRING_LIT(self, token):
        all_tokens.append(("T_STRINGLITERAL " + token))
        return "T_STRINGLITERAL " + token

    def OPERATOR_PUNC(self, token):
        all_tokens.append(token)
        return token

    def KEYWORDS(self, token):
        token = token.rstrip()
        all_tokens.append(token)
        return token

    def __default_token__(self, token):
        all_tokens.append(token)
        return super().__default_token__(token)


def new_lexer(string):
    string = replace_defines(string + ' ')
    all_tokens.clear()
    parser = Lark(rules, parser='lalr', transformer=T())
    parser.parse(string + ' ')
    return '\n'.join(all_tokens) + "\n"
