from phase1.student.compiler.main import run
from os import listdir


def join_path(path):
    return 'tests/test/in-out/' + path


step = 0

######################################
# by setting only_one_test to a value different from None it will test only that testcase
only_one_test = 3
######################################

for f in listdir('tests/test/in-out'):
    if f[-3:] == ".in":
        step += 1
        if only_one_test is not None and step != only_one_test:
            continue

        input = join_path(f)
        output = join_path(f[:-3] + ".out")
        t = run(input)
        print("#" * 50, "input test = ", step, "#" * 50)
        print(open(input).read())
        print("<" * 10 + "=" * 40, "our output test = ", step, "=" * 40 + ">" * 10)
        print(t)
        print("$" * 50, "answer test = ", step, "$" * 50)
        print(open(output).read())
