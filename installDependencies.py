import os
import sys
import platform

numpara = False

buildParaCode = True
buildTest = True

installDependencies = True
installPip = True
runRepl = False

args = sys.argv
if len(args) == 2:
    if args[1].lower() == "--installdeps":
        buildParaCode = False
        buildTest = False
        installDependencies = True
        runRepl = False
        installPip = False
    elif args[1].lower() == "--installpip":
        buildParaCode = False
        buildTest = False
        installDependencies = False
        runRepl = False
        installPip = True
    elif args[1].lower() == "--install":
        buildParaCode = False
        buildTest = False
        installDependencies = True
        runRepl = False
        installPip = True
    elif args[1].lower() == "--installall":
        buildParaCode = False
        buildTest = False
        installDependencies = True
        runRepl = False
        installPip = True
    elif args[1].lower() == "--buildtest":
        buildParaCode = True
        buildTest = True
        installDependencies = False
        runRepl = False
        installPip = False
    elif args[1].lower() == "--build":
        buildParaCode = True
        buildTest = False
        installDependencies = False
        runRepl = False
        installPip = False
    elif args[1].lower() == "--runrepl":
        buildParaCode = False
        buildTest = False
        installDependencies = False
        runRepl = True
        installPip = False

baseInstall = 'pip install'

def install(install):
    os.system(baseInstall + ' ' + install)
    return baseInstall + ' ' + install

if installPip:
    install('--upgrade pip')

if installDependencies:
    if numpara:
        try:
            import numpy
        except ImportError:
            install('numpy')

if buildParaCode:
    if buildTest:
        os.system('python setup.py sdist bdist_wheel')
        os.system('python -m twine upload --repository testpypi dist/*')
    else:
        os.system('python setup.py sdist bdist_wheel')
        os.system('python -m twine upload dist/*')

if runRepl:
    os.system('python main.py')
    