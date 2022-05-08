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
correct = 0
error = 0
total = 0

for step, name in enumerate(all_tests.keys()):
    total += 1
    try:
        answer = open(f"../tests/in-out/{name}.out").read()
        res = run(f"../tests/in-out/{name}.in")
        if res and answer == "OK":
            print("OK", step)
            correct += 1
        elif not res and answer != "OK":
            print("OK", step)
            correct += 1
        else:
            print("WRONG ", step)
    except:
        error += 1
        print("ERROR on", name)

print("total=", total, "Correct=", correct, "Wrong=", total-error-correct,"Error=", error)


step = int(input("which test to investigate?"))
name = list(all_tests.keys())[step]
answer = open(f"../tests/in-out/{name}.out").read()
text = open(f"../tests/in-out/{name}.in").read()
print(text)
print("name=", name)
print("answer=", answer)
print(parser(text))
