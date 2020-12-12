import sys

def Run():
    from ParaCode.shell import RunShell

    args = sys.argv
    if len(args) == 2:
        RunShell(args[1])
    else:
        RunShell("")