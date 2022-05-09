import re

from lark import Lark

json_parser = Lark(r"""
    program: macro* decl+
    macro: "import" ESCAPED_STRING
    decl: variable_decl | function_decl | class_decl | interface_decl
    variable_decl: variable ";"
    variable: type ident
    type: "int" | "double" | "bool" | "string" | ident | type "[]" 
    function_decl: type ident "(" formals ")" stmtblock | "void" ident "(" formals ")" stmtblock
    formals: variable ("," variable)+ |  variable | null
    class_decl: "class" ident ("extends" ident)? ("implements" ident ("," ident)*)? "{" field* "}"
    field: access_mode variable_decl | access_mode function_decl
    access_mode: "private" | "public" | "protected" | null
    interface_decl: "interface" ident "{" prototype* "}"
    prototype: type ident "(" formals ");" | "void" ident "(" formals ");" 
    stmtblock: "{" variable_decl* stmt* "}"
    linestmtblock: variable_decl | stmt 
    stmt: expr? ";" | ifstmt | whilestmt | whilestmt | forstmt | breakstmt | continuestmt | returnstmt | printstmt | stmtblock     
    ifstmt: "if""(" expr ")" stmt ("else" stmt)?
    whilestmt: "while""(" expr ")" stmt
    forstmt: "for" "(" expr? ";" expr ";" expr? ")" stmt
    returnstmt: "return" expr? ";"
    breakstmt: "break;"
    continuestmt: "continue;"
    printstmt: "Print" "(" expr ("," expr)* ");"
    expr: lvalue "=" expr | lvalue "+=" expr | lvalue "-=" expr | constant | lvalue | "this" | call | "(" expr ")" | expr "-" expr | expr "+" expr
        | expr "*" expr | expr "/" expr | expr "%" expr | "-" expr | expr "<" expr | expr "<=" expr
        | expr ">" expr | expr ">=" expr | expr "==" expr | expr "!=" expr | expr "&&" expr | expr "||" expr
        | "!" expr | "ReadInteger()" | "readLine()" | "new" ident | "NewArray(" expr "," type ")" | "itod(" expr ")"
        | "dtoi(" expr ")" | "itob(" expr ")" | "btoi(" expr ")"  
    lvalue: ident | expr "." ident | expr "[" expr "]" 
    call: ident "(" actuals ")" | expr "." ident "(" actuals ")" 
    actuals: expr ("," expr)*  | null
    constant: doubleconstant | INT | boolconstant | ESCAPED_STRING | base16 | "null"
    null:
    ident: /[a-zA-Z][a-zA-Z0-9_]*/ | /__func__[a-zA-Z0-9_]*/ | /__line__[a-zA-Z0-9_]*/ 
    doubleconstant: /[0-9]+/"."/[0-9]+/ | /[0-9]+/"." | /[0-9]+/"."/[0-9]*[Ee][+-]?[0-9]+/
    boolconstant: "True" | "False"
    INT: /[0-9]+/
    base16: /0[xX][0-9a-fA-F]+/
    
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
""", start='program', parser='lalr')

def remove_comment(s):
    s=s.replace("//","@")
    s=re.sub("@[^\n]*","",s)
    s=s.replace("/*","#")
    s=s.replace("*/","@")
    s=re.sub("#[^#@]*@","",s)
    return s

def parser(string):
    string=remove_comment(string)
    return json_parser.parse(string)
print(parser(open(f"../tests/in-out/t006-function1.in").read()).pretty())

