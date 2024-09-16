import os
import webbrowser
import termcolor
from termcolor import colored
def display_logo() -> None:
    red = "\033[31m"
    purple = "\033[35m"
    cyan = "\033[36m"
    reset = "\033[0m"

    print("\033[H\033[2J\033[1m\033[36m                                                        ")
    print(f"{red}███████╗ █████╗ ██╗███████╗ █████╗ ███╗   ██╗    ███╗   ██╗███████╗████████╗{reset}")
    print(f"{red}██╔════╝██╔══██╗██║╚══███╔╝██╔══██╗████╗  ██║    ████╗  ██║██╔════╝╚══██╔══╝{reset}")
    print(f"{red}█████╗  ███████║██║  ███╔╝ ███████║██╔██╗ ██║    ██╔██╗ ██║█████╗     ██║   {reset}")
    print(f"{red}██╔══╝  ██╔══██║██║ ███╔╝  ██╔══██║██║╚██╗██║    ██║╚██╗██║██╔══╝     ██║   {reset}")
    print(f"{red}██║     ██║  ██║██║███████╗██║  ██║██║ ╚████║    ██║ ╚████║███████╗   ██║   {reset}")
    print(f"{red}╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝  ╚═══╝╚══════╝   ╚═╝   {reset}")
    print(f"{purple}                        MADE BY FAIZAN KHAN \n              INSTAGRAM: @EthicalFaizan GITHUB: @Faizan-Khanx {reset}")

def main_menu() -> None:
    while True:
        display_logo()
        print(colored("1) Subnet IPV4 & Scans All Hosts", 'cyan'))
        print(colored("2) Subnet IPV6", 'cyan'))
        print(colored("3) Socials", 'cyan'))
        print(colored("4) Exit", 'cyan'))
        choice = input(colored("\n[?] Choose an option from 1 to 4 : ", 'red')).strip()

        if choice == '1':
            os.system('python V4.py')
        elif choice == '2':
            os.system('python V6.py')
        elif choice == '3':
            socials_menu()
        elif choice == '4':
            print(colored("Exiting... Thank you!", 'green'))
            break
        else:
            print(colored("[!] Invalid choice. Please choose a valid option.", 'red'))

def socials_menu() -> None:
    while True:
        print(colored("\nWELCOME TO SOCIALS", 'yellow'))
        print(colored("1) More Useful Tools", 'cyan'))
        print(colored("2) LinkedIn", 'cyan'))
        print(colored("3) Instagram", 'cyan'))
        print(colored("4) Back", 'cyan'))
        choice = input(colored("\n[?] Choose an option from 1 to 4  ", 'red')).strip()

        if choice == '1':
            webbrowser.open('https://github.com/Faizan-Khanx')  # Open GitHub
        elif choice == '2':
            webbrowser.open('https://www.linkedin.com/in/EthicalFaizan')  # Replace with your LinkedIn URL
        elif choice == '3':
            webbrowser.open('https://www.instagram.com/EthicalFaizan')  # Replace with your Instagram URL
        elif choice == '4':
            break
        else:
            print(colored("[!] Invalid choice. Please choose a valid option.", 'red'))

if __name__ == '__main__':
    main_menu()

