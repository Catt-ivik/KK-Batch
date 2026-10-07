import sys
import os

def remove_first_line(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        if len(lines) > 0:
            with open(filename, 'w') as file:
                file.writelines(lines[1:])
        else:
            print(f"The file {filename} is empty.")
    except FileNotFoundError:
        print(f"The file {filename} doesn't exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Using: python script.py filename")
    else:
        filename = sys.argv[1]
        remove_first_line(filename)
