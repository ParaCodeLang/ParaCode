import subprocess
import sys

rcmd = "( find ./ -type d -name .git -prune -o -name '*.%s' -not -path './build/**' -print0 | xargs -0 cat ) | wc {}"
types = ['c', 'cpp', 'h', 'hpp', 'rs', 'py', 'para', 'paracode', 'sh']

if len(sys.argv) > 1:
    if sys.argv[1].lower() == "lines":
        rcmd = rcmd.format("-l")
    elif sys.argv[1].lower() == "chars":
        rcmd = rcmd.format("-c")
    elif sys.argv[1].lower() == "maxlinelength" or sys.argv[1].lower(
    ) == "max-line-length" or sys.argv[1].lower() == "mll":
        rcmd = rcmd.format("-L")
    elif sys.argv[1].lower() == "files":
        rcmd = "( find ./ -type d -name .git -prune -o -name '*.%s' -not -path './build/**' -print ) | wc -l"
    else:
        rcmd = rcmd.format("-l")
else:
    rcmd = rcmd.format("-l")

if len(sys.argv) > 2:
    if sys.argv[2].lower() == "c":
        types = ['c', 'h']
    elif sys.argv[2].lower() == "c++" or sys.argv[2].lower() == "cpp":
        types = ['cpp', 'h', 'hpp']
    elif sys.argv[2].lower() == "allc":
        types = ['c', 'cpp', 'h', 'hpp']
    elif sys.argv[2].lower() == "rust" or sys.argv[2].lower() == "rs":
        types = ['rs']
    elif sys.argv[2].lower() == "python" or sys.argv[2].lower() == "py":
        types = ['py']
    elif sys.argv[2].lower() == "paracode" or sys.argv[2].lower() == "para":
        types = ['para', 'paracode']
    elif sys.argv[2].lower() == "main":
        types = ['rs', 'py', 'para', 'paracode']
    elif sys.argv[2].lower() == "sh":
        types = ['sh']

sum = 0
for el in types:
    cmd = rcmd % (el)
    p = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    out = int(p.stdout.read().strip())
    print("*.%s: %s" % (el, out))
    sum += out
print("sum: %d" % (sum))
