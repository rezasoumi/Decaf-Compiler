from os import listdir

from phase1.student.compiler.lexer import new_lexer
from phase2.compiler.parser import parser


def run(input_file_address: str) -> bool:
    input_file = open(input_file_address)
    input_content = input_file.read()
    try:
        parser(input_content)
        return True
    except:
        return False


all_tests = {}
for f in listdir('../tests/in-out'):
    all_tests[f.split('.')[0]] = True

for step, name in enumerate(all_tests.keys()):
    try:
        answer = open(f"../tests/in-out/{name}.out").read()
        res = run(f"../tests/in-out/{name}.in")
        if res and answer == "OK":
            print("OK", step)
        elif not res and answer != "OK":
            print("OK", step)
        else:
            print("WRONG ", step)
    except:
        print("ERROR on", name)

while True:
    step = int(input())
    name = list(all_tests.keys())[step]
    answer = open(f"../tests/in-out/{name}.out").read()
    res = run(f"../tests/in-out/{name}.in")
    print(open(f"../tests/in-out/{name}.in").read())
    print("name=", name)
    print("answer=", answer)
    print("our result=", res)
