from lark import Lark
from lark import Transformer
# you can write here and import this file in main!
rules = """
    start : (ID | OPERATOR_PUNC | KEYWORDS | BOOLEAN_LIT | INT_LIT | DOUBLE_LIT)*
    ID: /[a-zA-Z][a-zA-Z0-9_]*/
    OPERATOR_PUNC: "+" | "-" | "*" | "/" | "%" | "<" | "<=" | ">" | ">=" | "=" 
                    | "+=" | "-+" | "*=" | "/=" | "==" | "!=" | "&&" |  "||" 
                    | "!" | ";" | "," | "." | "[" | "]" | "(" | ")" | "{" | "}"  
    
    KEYWORDS: "__func__" | "__line__" | "bool" | "break" | "btoi" | "class" | "continue" 
                | "double" | "dtoi" | "else" | "for" | "if" | "import" | "int" | "itob" 
                | "itod" | "new" | "NewArray" | "null" | "Print" | "private" | "public" 
                | "ReadInteger" | "ReadLine" | "return" | "string" | "this" | "void" | "while"
    
    BOOLEAN_LIT: "true" | "false" 
    INT_LIT : /0[Xx][0-9a-fA-F]+/ | /[0-9]+/
    DOUBLE_LIT : /[0-9]+\\.[0-9]*/ | /[0-9]+\\.[0-9]*[Ee][+-]?[0-9]+/
    
    %import common.WS -> WS
    %ignore WS
"""
all_tokens = []
class T(Transformer):
    def ID(self, token):
        all_tokens.append(("T_ID " + token))
        return "T_ID " + token
    def BOOLEAN_LIT(self, token):
        all_tokens.append(("T_BOOLEANLITERAL " + token))
        return "T_BOOLEANLITERAL " + token
    def INT_LIT(self , token):
        all_tokens.append(("T_INTLITERAL " + token))
        return "T_INTLITERAL " + token
    def DOUBLE_LIT(self , token):
        all_tokens.append(("T_DOUBLELITERAL " + token))
        return "T_DOUBLELITERAL " + token
    def OPERATOR_PUNC(self , token):
        all_tokens.append( token)
        return token
    def KEYWORDS(self , token):
        all_tokens.append(token)
        return token
    def __default_token__(self, token):
        all_tokens.append(token)
        return super().__default_token__(token)

def new_lexer(string):
    all_tokens.clear()
    parser = Lark(rules, parser='lalr', transformer = T())
    parser.parse(string)
    return '\n'.join(all_tokens)

