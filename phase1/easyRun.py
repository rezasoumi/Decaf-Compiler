from phase1.student.compiler.main import run
from os import listdir


def join_path(path):
    return 'tests/test/in-out/' + path


step = 0

######################################
# by setting only_one_test to a value different from None it will test only that testcase
tests = None #[8,10]
######################################

for f in listdir('tests/test/in-out'):
    if f[-3:] == ".in":
        step += 1
        if tests is not None and step not in tests:
            continue

        input = join_path(f)
        output = join_path(f[:-3] + ".out")
        t = run(input).rstrip()
        answer = open(output).read().rstrip()

        if answer != t:
            print("#" * 50, "input test = ", step, "#" * 50)
            print(open(input).read())
            print("<" * 10 + "=" * 40, "our output test = ", step, "=" * 40 + ">" * 10)
            print(t)
            print("$" * 50, "answer test = ", step, "$" * 50)
            print(answer)
            print("@" * 50, "diff test = ", step, "@" * 50)
            outputList = answer.split('\n')
            tList = t.split('\n')
            for i in range(len(outputList)):
                if len(tList) > i and outputList[i] != tList[i]:
                    print(i, "\t", tList[i], "   ==>  ", outputList[i])
                if len(tList) <= i:
                    print(i, "\t", "nothing", "   ==>  ", outputList[i])
        else:
            print("pass test", step)
