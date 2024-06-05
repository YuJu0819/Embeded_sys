def print_help():
    print("\nGeneral mode commands:")
    # print("  - add <num1> <num2>: Add two numbers")
    # print("  - subtract <num1> <num2>: Subtract num2 from num1")
    # print("  - multiply <num1> <num2>: Multiply two numbers")
    # print("  - divide <num1> <num2>: Divide num1 by num2")
    print("  - list_read(lr) <file> : Read the list of participants from a file")
    print("  - list_confirm(lc)     : Confirm the attendance of the participants in the list")
    print("  - list_print(lp) [-y][-n]")     
    print("          -y             : Print the list of participants who has confirmed their attendance")
    print("          -n             : Print the list of participants who has not confirmed their attendance\n")
    print("  - mode(m)              : Display the current mode (general/meeting/voting)")
    print("  - mode(m) [-s <mode>]  : Switch to the mode <mode> (general/meeting/voting) [default = general]")
    print("  - help(h)              : Display this help message")
    print("  - quit(q)              : Exit the program")

    print("\nVoting mode commands:")
    print("  - vote [-pr][-ps][-v][-q][-t <time>][-s <topic>][-w <file>] ")
    print("          -pr            : Print the voting results")
    print("          -ps            : Print the settings of the current vote")
    print("          -v             : Start the voting process for <time> seconds")
    print("          -q             : quit the voting mode")
    print("          -t <time>      : Set the voting duration in seconds [default = 60]")
    print("          -s <topic>     : Set the voting topic")
    print("          -w <file>      : Write the voting results to a file")


    print("\nMeeting mode commands:")
    print("  - mic [-l][-p][-q][-t <time>][-s <id>] ")
    print("          -l             : listen whether there are any participants want to speak for <time> seconds timeout")
    print("          -p             : Print the id of current speaker")
    print("          -q             : quit the meeting mode")
    print("          -t <time>      : Set the timeout for listening to <time> seconds [default = 60]")
    print("          -s <id>        : Switch the current speaker to the speaker with id <id>")
