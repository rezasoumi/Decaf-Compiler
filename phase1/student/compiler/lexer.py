from lark import Lark
from lark import Transformer
# you can write here and import this file in main!

rules = """
    start : (ID)*
    ID: /[a-zA-Z][a-zA-Z0-9_]*/
    Operator_Punctuataion: [+|-|*|/|%|<|<=|>|>=|=|+=|-+|*=|/=|==|!=|&&||||!|;|,|.|[|]|(|)|{|}] # + - * / % < <= > >= = += -+ *= /= == != && || ! ; , . [ ] ( ) { }
    Keywords: [__func__|__line__|bool|break|btoi|class|continue|double|dtoi|else|for|if|import|int|itob|itod|new|NewArray|null|Print|private|public|ReadInteger|ReadLine|return|string|this|void|while]
    %import common.WS -> WS
    %ignore WS
"""
all_tokens = []

class T(Transformer):
    def ID(self, token):
        all_tokens.append(("T_ID " + token))
        return "T_ID " + token
    def Operator_Punctuataion(self, token):
        all_tokens.append((token))
        return token
    def Keywords(self, token):
        all_tokens.append((token))
        return token
def new_lexer(string):
    all_tokens.clear()
    parser = Lark(rules, parser='lalr', transformer = T())
    parser.parse(string)
    return '\n'.join(all_tokens)

