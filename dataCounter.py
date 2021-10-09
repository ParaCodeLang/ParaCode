import subprocess
import sys
import os

rcmd = "( find ./ -name '*.%s' -print0 | xargs -0 cat ) | wc -l"
types = ['c', 'cpp', 'h', 'hpp', 'py', 'para', 'paracode', 'go', 'sh']

if len(sys.argv) > 1:
    if sys.argv[1].lower() == "lines":
        rcmd = "( find ./ -name '*.%s' -print0 | xargs -0 cat ) | wc -l"
    elif sys.argv[1].lower() == "words":
        rcmd = "( find ./ -name '*.%s' -print0 | xargs -0 cat ) | wc -w"
    elif sys.argv[1].lower() == "chars":
        rcmd = "( find ./ -name '*.%s' -print0 | xargs -0 cat ) | wc -m"
    elif sys.argv[1].lower() == "bytes":
        rcmd = "( find ./ -name '*.%s' -print0 | xargs -0 cat ) | wc -c"
    elif sys.argv[1].lower() == "maxlinelength" or sys.argv[1].lower() == "max-line-length" or sys.argv[1].lower() == "mll":
        rcmd = "( find ./ -name '*.%s' -print0 | xargs -0 cat ) | wc -L"
    
if len(sys.argv) > 2:
    if sys.argv[2].lower() == "c":
        types = ['c', 'h']
    elif sys.argv[2].lower() == "c++" or sys.argv[2].lower() == "cpp":
        types = ['cpp', 'h', 'hpp']
    elif sys.argv[2].lower() == "allc":
        types = ['c', 'cpp', 'h', 'hpp']
    elif sys.argv[2].lower() == "python" or sys.argv[2].lower() == "py":
        types = ['py']
    elif sys.argv[2].lower() == "paracode" or sys.argv[2].lower() == "para":
        types = ['para', 'paracode']
    elif sys.argv[2].lower() == "main":
        types = ['c', 'cpp', 'h', 'hpp', 'py', 'para', 'paracode']
    elif sys.argv[2].lower() == "go":
        types = ['go']
    elif sys.argv[2].lower() == "sh":
        types = ['sh']

sum = 0
for el in types:
    if len(sys.argv) > 1 and sys.argv[1].lower() != "files":
        cmd = rcmd % (el)
        p = subprocess.Popen([cmd],stdout=subprocess.PIPE,shell=True)
        out = int(p.stdout.read().strip())
        print("*.%s: %s" % (el, out))
        sum += out
    else:
        out = 0
        for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
            for file in files:
                if file.endswith("." + el):
                    out += 1
        print("*.%s: %s" % (el, out))
        sum += out
print("sum: %d" % (sum))
