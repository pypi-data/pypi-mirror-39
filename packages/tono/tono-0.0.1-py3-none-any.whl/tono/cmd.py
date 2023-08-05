import sys

def jalani_cmd():
    command = sys.argv
    try:
        arg = command[1]
    except:
        arg = "Wellcome to pybie"

    print(arg)