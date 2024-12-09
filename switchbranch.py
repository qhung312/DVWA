#!/usr/bin/env python3

import subprocess

# Location of compose file that we're targeting
COMPOSE_FILE = "compose.yml"


# Run shell command and return output
def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
        exit(1)

    return result.stdout.strip()


# Get all available git branches
def get_branches():
    return run_command("git branch --format='%(refname:short)'").split("\n")


# Stop running DVWA containers
def stop_docker_compose():
    return run_command("docker compose -f {} down".format(COMPOSE_FILE))


# Start DVWA containers
# This should be called after switching branch
def start_docker_compose():
    return run_command("docker compose -f {} up -d".format(COMPOSE_FILE))


# Change current branch
def checkout_to_branch(branch):
    return run_command("git checkout {}".format(branch))


if __name__ == "__main__":
    branches = get_branches()

    # Displays all branches and ask user to select one
    user_choice = -1
    while user_choice <= 0 or user_choice > len(branches):
        print("Available branches:")
        for i, branch in enumerate(branches):
            print(f"{i + 1}: {branch}")

        try:
            user_choice = int(input("Select a branch (enter number): "))
        except ValueError:
            print("Invalid input. Please enter a number.")

    selected_branch = branches[user_choice - 1]

    # Move over to alternative implementations of DVWA
    stop_docker_compose()
    checkout_to_branch(selected_branch)
    start_docker_compose()

    print(f"Switched to branch: {selected_branch}")
