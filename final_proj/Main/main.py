import argparse
from cmd.help import print_help
from cmd.vote import vote_count
from server.command_client import send_message
import pandas as pd


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
        elif command == "list_print" or command == "lp":
            try:
                if Input[1] == "-y":
                    # print the row with no at last element
                    df = pd.read_csv('server/meeting_database.csv')
                    print(df[df.iloc[:,1] == "arrive"])
                elif Input[1] == "-n":
                    df = pd.read_csv('server/meeting_database.csv')
                    print(df[df.iloc[:,1] == "No"])
                else:
                    print("Invalid command. Please try again or type 'help' for assistance.")
            except IndexError:
                df = pd.read_csv('server/meeting_database.csv')
                print(df)
            continue
        elif command == "mode" or command == "m":
            try:
                if Input[1] == "-s":
                    if mode == "meeting":
                        print("Switch to general mode")
                        mode = "general"
                        send_message(port, f"end")
                    elif mode == "general":
                        print("Switch to meeting mode")
                        mode = "meeting"
                        send_message(port, f"start")
                    else: 
                        print("Invalid mode argument. Please try again or type 'help' for assistance.")
                else:
                    print("Invalid command. Please try again or type 'help' for assistance.")
            except IndexError:
                print("The current mode is: ", mode)
            continue
        elif command == "vote" or command == "v":
            if mode != "meeting":
                print("Wrong mode. Please switch to meeting mode by typing 'mode -s' first.")
                continue
            try:
                if Input[1] == "-pr":
                    print("The voting results are: ", vote_count())
                elif Input[1] == "-ps":
                    print("Print the settings of the current vote")
                elif Input[1] == "-v":
                    print("Start the voting process for: ", issue)
                    send_message(port, f"voting {issue} {voting_duration}")
                elif Input[1] == "-t":
                    voting_duration = int(Input[2])
                    print("Set the voting duration in seconds to", Input[2])
                elif Input[1] == "-s":
                    print("Set the voting topic to", Input[2])
                    issue = Input[2]
                elif Input[1] == "-w":
                    print("Write the voting results to a file", Input[2])
                else:
                    print("Invalid command. Please try again or type 'help' for assistance.")
            except IndexError:
                print("Invalid command. Please try again or type 'help' for assistance.")
        elif command == "mic":
            if mode != "meeting":
                print("Wrong mode. Please switch to meeting mode by typing 'mode -s' first.")
                continue
            try:
                if Input[1] == "-l":
                    print("Start listening ...")
                    send_message(port, f"speaking {mic_timeout}")
                elif Input[1] == "-p":
                    print("Print the id of the current speaker")
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
