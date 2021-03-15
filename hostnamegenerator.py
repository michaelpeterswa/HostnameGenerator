#!/usr/bin/python3

import os
import inquirer
from pyfiglet import Figlet
import json

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

def load_data():
    with open("data/sorted_by_distance.json", "r") as data:
       return json.load(data)

def view():
    for line in data[:10]:
        print(line["name"])

def create():
    print('create')

def edit():
    print('edit')

def delete():
    print('delete')

def main():
    clear()
    title()
    intro_answers = intro()
    
    clear()
    title()
    if intro_answers["result"] == "View":
        view()
        
    elif intro_answers["result"] == "Quit":
        exit(0)

if __name__ == "__main__":
    data = load_data()
    main()