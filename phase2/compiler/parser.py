from lark import Lark

json_parser = Lark(r"""
    program: macro* decl+
    macro: "import" ESCAPED_STRING
    decl: variable_decl | function_decl | class_decl | interface_decl
    variable_decl: variable ";"
    variable: type ident
    type: "int" | "double" | "bool" | "string" | ident | type "[]" 
    function_decl: type ident "(" formals ")" stmtblock | "void" ident "(" formals ")" stmtblock
    formals: ("," variable)+ | null
    class_decl: "class" ident ("extends" ident)? ("implements" ("," ident)+)? "{" field* "}"
    field: access_mode variable_decl | access_mode function_decl
    access_mode: "private" | "public" | "protected" | null
    interface_decl: "interface" ident "{" prototype* "}"
    prototype: type ident "(" formals ");" | "void" ident "(" formals ");" 
    stmtblock: "{" variable_decl* stmt* "}"
    stmt: expr? ";" | ifstmt | whilestmt | whilestmt | forstmt | breakstmt | continuestmt | returnstmt | printstmt | stmtblock     
    ifstmt: "if(" expr ")" stmt ("else" stmt)?
    whilestmt: "while(" expr ")" stmt
    forstmt: "for(" expr? ";" expr ";" expr? ")" stmt
    returnstmt: "return" expr? ";"
    breakstmt: "break;"
    continuestmt: "continue;"
    printstmt: "print" ("," expr)+
    expr: lvalue "=" expr | lvalue "+=" expr | lvalue "-=" expr | constant | lvalue | "this" | call | "(" expr ")" | expr "-" expr | expr "+" expr
        | expr "*" expr | expr "/" expr | expr "%" expr | "-" expr | expr "<" expr | expr "<=" expr
        | expr ">" expr | expr ">=" expr | expr "==" expr | expr "!=" expr | expr "&&" expr | expr "||" expr
        | "!" expr | "ReadInteger()" | "readLine()" | "new" ident | "NewArray(" expr "," type ")" | "itod(" expr ")"
        | "dtoi(" expr ")" | "itob(" expr ")" | "btoi(" expr ")"  
    lvalue: ident | expr "." ident | "expr[" expr "]" 
    call: ident "(" actuals ")" | expr "." ident "(" actuals ")" 
    actuals: ("," expr)+  | null
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

def parser(string):
    return json_parser.parse(string)

# parser("int x;")
