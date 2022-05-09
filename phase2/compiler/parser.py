import re

from lark import Lark

from phase1.student.compiler.lexer import replace_defines

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
    breakstmt: "break" ";"
    continuestmt: "continue" ";"
    printstmt: "Print" "(" expr ("," expr)* ")" ";"
    expr: lvalue "=" expr | lvalue "+=" expr | lvalue "*=" expr | lvalue "/=" expr | lvalue "-=" expr | constant | lvalue | "this" | call | "(" expr ")" | expr "-" expr | expr "+" expr
        | expr "*" expr | expr "/" expr | expr "%" expr | "-" expr | expr "<" expr | expr "<=" expr
        | expr ">" expr | expr ">=" expr | expr "==" expr | expr "!=" expr | expr "&&" expr | expr "||" expr
        | "!" expr | "ReadInteger()" | "ReadLine()" | "new" ident | "NewArray" "(" expr "," type ")" | "itod(" expr ")"
        | "dtoi(" expr ")" | "itob(" expr ")" | "btoi(" expr ")"  
    lvalue: ident | expr "." ident | expr "[" expr "]" 
    call: ident "(" actuals ")" | expr "." ident "(" actuals ")" 
    actuals: expr ("," expr)* | null
    constant: doubleconstant | INT | boolconstant | ESCAPED_STRING | base16 | "null"
    null:
    ident: /@[a-zA-Z][a-zA-Z0-9_]*/ | /@__func__[a-zA-Z0-9_]*/ | /@__line__[a-zA-Z0-9_]*/ 
    doubleconstant: /[0-9]+/"."/[0-9]+/ | /[0-9]+/"." | /[0-9]+/"."/[0-9]*[Ee][+-]?[0-9]+/
    boolconstant: "true" | "false"
    base16: /0[xX][0-9a-fA-F]+/
    INT: /[0-9]+/
    
    
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
""", start='program', parser='lalr')


def remove_comment(s):
    s = s.replace("//", "@")
    s = re.sub("@[^\n]*", "", s)
    s = s.replace("/*", "#")
    s = s.replace("*/", "@")
    s = re.sub("#[^#@]*@", "", s)
    return s


def reprep(string):
    keywords = "true, false, return, void, int, double, bool, string, class, interface, null, this, extends, implements, for, while, if, else, return, break, continue, new, NewArray, Print, ReadInteger, ReadLine, dtoi, itod, btoi, itob, private, protected, public, import".split(
        ", ")
    if string not in keywords and (re.match("[a-zA-Z][a-zA-Z0-9_]*",string) or re.match("__func__[a-zA-Z0-9_]*",string) or re.match("__line__[a-zA-Z0-9_]*",string)):
        return "@"+string
    else:
        return string


def replace_ident(string):
    stopWords=['.',' ','\n',']','[','(',')',';','!','-']
    ans = ""
    current = ""
    for i in range(len(string)):
        if string[i] in stopWords:
            ans += reprep(current)
            current = ""
            ans += string[i]
        else:
            current += string[i]
    ans += reprep(current)

    return ans


def parser(string):
    # string = replace_defines(string + ' ')
    string = remove_comment(string)
    string = string.replace(");", ") ;")
    string = replace_ident(string)
    string = re.sub("\[[ ]+\]",'[]',string)
    print(string)
    return json_parser.parse(string)


print(parser(open(f"../tests/in-out/myfile.in").read()).pretty())
