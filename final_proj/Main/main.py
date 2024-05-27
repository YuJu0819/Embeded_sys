import argparse
from cmd.help import print_help
from cmd.vote import vote_count
from server.command_client import send_message

def main():
    mode = "general"
    port = 5000
    issue = ""
    voting_duration = 60 # default voting duration (seconds)
    mic_timeout = 60 # default mic timeout (seconds)
    
    while True:
        Input = input("cube> ").strip().lower().split()
        command = Input[0]

        if command == "quit" or command == "q":
            print("Exiting the program.")
            break
        elif command == "help" or command == "h":
            print_help()
            continue
        elif command == "list_read" or command == "lr":
            continue
        elif command == "list_confirm" or command == "lc":
            continue
        elif command == "list_print" or command == "lp":
            try:
                if Input[1] == "-y":
                    print("Print the list of participants who have confirmed their attendance")
                elif Input[1] == "-n":
                    print("Print the list of participants who have not confirmed their attendance")
                else:
                    print("Invalid command. Please try again or type 'help' for assistance.")
            except IndexError:
                print("Invalid command. Please try again or type 'help' for assistance.")
            continue
        elif command == "mode" or command == "m":
            try:
                if Input[1] == "-s":
                    try:
                        if Input[2] == "general" or Input[2] == "meeting" or Input[2] == "voting":
                            print("Switch to the mode", Input[2])
                            send_message(port, f"{mode}, {issue}")
                            mode = Input[2]
                        else: 
                            print("Invalid mode argument. Please try again or type 'help' for assistance.")
                    except IndexError:
                        print("Missing mode argument after '-s'")
                else:
                    print("Invalid command. Please try again or type 'help' for assistance.")
            except IndexError:
                print("The current mode is: ", mode)
            continue
        elif command == "vote" or command == "v":
            if mode != "voting":
                print("Wrong mode. Please switch to voting mode by typing 'mode -s voting' first.")
                continue
            try:
                if Input[1] == "-pr":
                    print("The voting results are: ", vote_count())
                elif Input[1] == "-ps":
                    print("Print the settings of the current vote")
                elif Input[1] == "-v":
                    print("Start the voting process for: ")
                elif Input[1] == "-q":
                    mode = "general"
                    print("Quit the voting mode")
                elif Input[1] == "-t":
                    voting_duration = int(Input[2])
                    print("Set the voting duration in seconds to", Input[2])
                elif Input[1] == "-s":
                    print("Set the voting topic to", Input[2])
                elif Input[1] == "-w":
                    print("Write the voting results to a file", Input[2])
                else:
                    print("Invalid command. Please try again or type 'help' for assistance.")
            except IndexError:
                print("Invalid command. Please try again or type 'help' for assistance.")
        elif command == "mic":
            if mode != "meeting":
                print("Wrong mode. Please switch to meeting mode by typing 'mode -s meeting' first.")
                continue
            try:
                if Input[1] == "-l":
                    print("Listen whether there are any participants want to speak for: ")
                elif Input[1] == "-p":
                    print("Print the id of the current speaker")
                elif Input[1] == "-q":
                    mode = "general"
                    print("Quit the meeting mode")
                elif Input[1] == "-t":
                    mic_timeout = int(Input[2])
                    print("Set the timeout for listening to", Input[2], "seconds")
                elif Input[1] == "-s":
                    print("Switch the current speaker to the speaker with id", Input[2])
                else:
                    print("Invalid command. Please try again or type 'help' for assistance.")
            except IndexError:
                print("Invalid command. Please try again or type 'help' for assistance.")
        else:
            print("Invalid command. Please try again or type 'help' for assistance.")
            continue

if __name__ == "__main__":
    main()
