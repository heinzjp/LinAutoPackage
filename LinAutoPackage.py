import subprocess
import time
import sys
import os
from termcolor import colored

vaildOptions = ["-h", "-y", "-s", "-q"]

def printHelp():
    print("List of Options:\n"
          "-h : Displays help information\n"
          "-y : Force auto yes for installing packages\n"
          "-s : Simulate install"
          "-q : Suppress output from apt"
          )
    return

def checkArgs(args):
    numOfArgs = len(args)
    if numOfArgs == 0:
        print("Usage: python3 LinAutoPackage.py [OPTIONS] [FILE]")
        print("Use -h for help")
        return (False, '', "")
    
    if numOfArgs == 1 and args[0] == "-h":
        return (False, "-h", "")

    switches = ""
    forceReturn = False
    for x in range(0, numOfArgs -1):
        if args[x] not in vaildOptions:
            forceReturn = True
            print(args[x] + " is not supported\n"
                  "Use -h for help"
                  )
        else:
            switches += args[x] + " "
    if forceReturn:
        return (False, switches, "")
    
    filePath = sys.argv[len(args)]
    if not os.path.isfile(filePath):
        print(filePath + " is not a vaild file")
        return (False, switches, "")
    
    return (True, switches, filePath)

def doWork(switches, filePath):
    startTime = time.perf_counter()
    f = open(filePath, "r")
    list = []
    for x in f:
        try:
            print("Installing: " + x.strip())
            if "-q" in switches:
                subprocess.run(["sudo apt install " + switches + x], shell=True, check=True,
                               stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            else:
                subprocess.run(["sudo apt install " + switches + x], shell=True, check=True)
        except subprocess.CalledProcessError:
            list.append(x)
            print(colored('FAILED to install: ' + x.strip(), 'red'))
    
    endTime = time.perf_counter()
    print(f"Downloaded in {endTime - startTime:0.4f} seconds")

    if list:
        print(colored('PACKAGES NOT INSTALLED:', 'red'))
        for x in list:
            print(colored(x.strip(), 'red'))
    else:
        print(colored('All packages installed', 'green'))
    return

def main():
    args = sys.argv[1:]
    (isReturn, switches, filePath) = checkArgs(args)
    
    if "-h" in switches:
        printHelp()
        return

    if not isReturn:
        return
    
    doWork(switches, filePath)
    return

if __name__ == "__main__":
    main()