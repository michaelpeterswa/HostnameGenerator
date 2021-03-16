#!/usr/bin/python3

import os
import inquirer
import logging
from pyfiglet import Figlet
import json
from tabulate import tabulate

clear = lambda: os.system("clear")

def title():
    f = Figlet(font='smslant')
    print(f.renderText('HostGen'), "v1.0.0\n")

def intro():
    questions = [
        inquirer.List('result',
                    message="What would you like to do?",
                    choices=['View', 'Create', 'Edit', 'Delete', 'Quit'],
                ),
    ]
    return inquirer.prompt(questions)

def load_distance_data():
    with open("data/sorted_by_distance.json", "r") as data:
       return json.load(data)

def view(data):
    headers = 'keys'
    if not data:
        print("No hostnames assigned.\n")
    elif data:
        print(tabulate(data, headers), "\n")
    else:
        logging.warning("Shouldn't be possible to get here. Exiting!")
        exit(1)

    loop_to_main()

def create():
    curr = [data["hostname"] for data in current_associations]
    top_ten = [data["name"] for data in distance_data[:10+len(curr)] if data["name"] not in curr]
    questions = [
        inquirer.List('hostname',
                message="Select a hostname",
                choices=top_ten,
            ),
        inquirer.Text('ip',
                    message="What IP will you associate with {hostname}?"),
        inquirer.Text('description',
                    message="Please enter a short description")
    ]

    return inquirer.prompt(questions)

def edit():
    choice = [data["hostname"] for data in current_associations]
    questions = [
        inquirer.List('hostname',
                message="Select a hostname",
                choices=choice,
            ),
        inquirer.Text('ip',
                    message="What IP will you associate with {hostname}?"),
        inquirer.Text('description',
                    message="Please enter a short description")
    ]

    new_answer = inquirer.prompt(questions)

    for i, assoc in enumerate(current_associations):
        if assoc["hostname"] == new_answer["hostname"]:
            current_associations[i] = new_answer

def delete():
    choice = [data["hostname"] for data in current_associations]
    questions = [
        inquirer.List('hostname',
                message="Select a hostname",
                choices=choice,
            )
    ]

    new_answer = inquirer.prompt(questions)

    for i, assoc in enumerate(current_associations):
        if assoc["hostname"] == new_answer["hostname"]:
            del current_associations[i]

def loop_to_main():
    input("Press Enter to Continue...")
    main()

def main():
    clear()
    title()
    intro_answers = intro()
    
    clear()
    title()
    if intro_answers["result"] == "View":
        view(current_associations)

    elif intro_answers["result"] == "Create":
        current_associations.append(create())
        loop_to_main()
    
    elif intro_answers["result"] == "Edit":
        edit()
        loop_to_main()
    
    elif intro_answers["result"] == "Delete":
        delete()
        loop_to_main()
        
    elif intro_answers["result"] == "Quit":
        print("Exiting!\n")
        exit(0)
    
    else:
        logging.warning("Shouldn't be possible to get here. Exiting!")
        exit(1)


if __name__ == "__main__":
    current_associations = []
    logging.basicConfig(level=logging.DEBUG)
    distance_data = load_distance_data()
    main()