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
        answer += line + "\n"
        split_form = line.split()
        if len(split_form) == 3 and split_form[0] == 'define':
            define_map[split_form[1]] = split_form[2]
    return answer


rules = """
    start : (ID)*
    ID: /[a-zA-Z][a-zA-Z0-9_]*/
    Operator_Punctuation: [+|-|*|/|%|<|<=|>|>=|=|+=|-+|*=|/=|==|!=|&&||||!|;|,|.|[|]|(|)|{|}] # + - * / % < <= > >= = += -+ *= /= == != && || ! ; , . [ ] ( ) { }
    Keywords: [__func__|__line__|bool|break|btoi|class|continue|double|dtoi|else|for|if|import|int|itob|itod|new|NewArray|null|Print|private|public|ReadInteger|ReadLine|return|string|this|void|while]
    %import common.WS -> WS
    %ignore WS
"""
all_tokens = []


class T(Transformer):
    def ID(self, token):
        all_tokens.append(("T_ID " + token))
        return "T_ID " + token

    def Operator_Punctuation(self, token):
        all_tokens.append((token))
        return token

    def Keywords(self, token):
        all_tokens.append((token))
        return token


def new_lexer(string):
    all_tokens.clear()
    parser = Lark(rules, parser='lalr', transformer=T())
    parser.parse(string)
    return '\n'.join(all_tokens)
