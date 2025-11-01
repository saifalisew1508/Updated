import asyncio
import pickle
import os
from time import sleep
from colorama import init, Fore

# Import from new location
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError

try:
    import requests
except ImportError:
    print(f'{Fore.LIGHTGREEN_EX}[i] Installing module - requests...{Fore.RESET}')
    os.system('pip install requests')

init()

n = Fore.RESET
lg = Fore.LIGHTGREEN_EX
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [lg, r, w, cy, ye]

# --- Your API Credentials ---
# Moved here for easy access
API_ID = 3910389
API_HASH = '86f861352f0ab76a251866059a6adbd6'
# --------------------------

def banner():
    import random
    # fancy logo
    b = [
    '░██████╗███████╗████████╗██╗░░░██╗██████╗░',
    '██╔════╝██╔════╝╚══██╔══╝██║░░░██║██╔══██╗',
    '╚█████╗░█████╗░░░░░██║░░░██║░░░██║██████╔╝',
    '░╚═══██╗██╔══╝░░░░░██║░░░██║░░░██║██╔═══╝░',
    '██████╔╝███████╗░░░██║░░░╚██████╔╝██║░░░░░',
    '╚═════╝░╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░░░'
    ]
    for char in b:
        print(f'{random.choice(colors)}{char}{n}')
    print('Contact below address for get premium script')
    # Fixed 'rs' variable to 'n'
    print(f'{lg}Version: {w}2.0{lg} | GitHub: {w}@saifalisew1508{n}')
    print(f'{lg}Telegram: {w}@DearSaif{lg} | Instagram: {w}@_Prince.Babu_{n}')

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

async def login_account(phone):
    """
    Asynchronously logs in a single account and saves the session.
    """
    print(f'{lg}[*] Logging in from {phone}{n}')
    # Use async with for automatic connection/disconnection
    try:
        async with TelegramClient(f'sessions/{phone}', API_ID, API_HASH) as client:
            # Start will prompt for code interactively if needed
            await client.start(phone=phone)
            print(f'{lg}[+] Login successful for {phone}{n}')
    except Exception as e:
        print(f'{r}[!] Failed to login {phone}: {e}{n}')

async def check_account(phone):
    """
    Asynchronously checks if an account is banned.
    Returns True if banned, False otherwise.
    """
    client = TelegramClient(f'sessions/{phone}', API_ID, API_HASH)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            # If not authorized, try to send code. This is where ban error occurs.
            await client.send_code_request(phone)
            print(f'{lg}[+] {phone} is not banned (needs code).{n}')
        else:
            print(f'{lg}[+] {phone} is active and authorized.{n}')
        return False  # Not banned
    except PhoneNumberBannedError:
        print(f'{r}[!] {phone} is BANNED!{n}')
        return True  # Banned
    except Exception as e:
        # Handle other errors like session file corruption, etc.
        print(f'{r}[!] Error checking {phone}: {e}{n}')
        return False  # Assume not banned on other errors
    finally:
        if client.is_connected():
            await client.disconnect()

# Main script loop
while True:
    clr()
    banner()
    print(f'{lg}[1] Add new accounts{n}')
    print(f'{lg}[2] Filter all banned accounts{n}')
    print(f'{lg}[3] Delete specific accounts{n}')
    print(f'{lg}[4] Update your Script{n}')
    print(f'{lg}[5] Display All Accounts{n}')
    print(f'{lg}[6] Quit{n}')
    
    try:
        a = int(input('\nEnter your choice: '))
    except ValueError:
        print(f'{r}[!] Invalid choice. Please enter a number.{n}')
        sleep(2)
        continue

    if a == 1:
        new_accs = []
        with open('vars.txt', 'ab') as g:
            try:
                number_to_add = int(input(f'\n{lg} [~] Enter How Many Accounts You Want To Add: {r}'))
            except ValueError:
                print(f'{r}[!] Invalid input. Please enter a number.{n}')
                sleep(2)
                continue
                
            for _ in range(number_to_add):
                phone_number = str(input(f'\n{lg} [~] Enter Phone Number With Country Code: {r}'))
                parsed_number = ''.join(phone_number.split())
                if not parsed_number.startswith('+'):
                    print(f'{r}[!] Phone number must start with country code (e.g., +123456...){n}')
                    continue
                pickle.dump([parsed_number], g)
                new_accs.append(parsed_number)
            print(f'\n{lg} [i] Saved all accounts in vars.txt')
            clr()
            print(f'\n{lg} [*] Logging in from new accounts\n')
            for number in new_accs:
                # Run the new async login function
                asyncio.run(login_account(number))
            input(f'\n Press enter to goto main menu...')
        # g.close() is not needed, 'with open' handles it.

    elif a == 2:
        accounts = []
        banned_accs = []
        try:
            with open('vars.txt', 'rb') as h:
                while True:
                    try:
                        accounts.append(pickle.load(h))
                    except EOFError:
                        break
        except FileNotFoundError:
            print(f'{r}[!] vars.txt not found. Please add accounts first.{n}')
            sleep(3)
            continue

        if not accounts:
            print(f'{r}[!] There are no accounts! Please add some and retry')
            sleep(3)
        else:
            print(f'{lg}[*] Checking all accounts...{n}')
            for account in accounts:
                phone = str(account[0])
                # Run the new async check function
                is_banned = asyncio.run(check_account(phone))
                if is_banned:
                    banned_accs.append(account)
            
            if not banned_accs:
                print(f'{lg}Congrats! No banned accounts')
            else:
                print(f'\n{r}[!] Removing {len(banned_accs)} banned accounts...{n}')
                for m in banned_accs:
                    accounts.remove(m)
                with open('vars.txt', 'wb') as k:
                    for a in accounts:
                        Phone = a[0]
                        pickle.dump([Phone], k)
                # k.close() is not needed
                print(f'{lg}[i] All banned accounts removed{n}')
            input('\nPress enter to goto main menu...')

    elif a == 3:
        accs = []
        try:
            with open('vars.txt', 'rb') as f:
                while True:
                    try:
                        accs.append(pickle.load(f))
                    except EOFError:
                        break
        except FileNotFoundError:
            print(f'{r}[!] vars.txt not found. No accounts to delete.{n}')
            sleep(3)
            continue

        if not accs:
            print(f'{r}[!] No accounts found in vars.txt.{n}')
            sleep(3)
            continue

        print(f'{lg}[i] Choose an account to delete\n')
        for i, acc in enumerate(accs):
            print(f'{lg}[{i}] {acc[0]}{n}')
        
        try:
            index = int(input(f'\n{lg}[+] Enter a choice: {n}'))
            if index < 0 or index >= len(accs):
                print(f'{r}[!] Invalid choice.{n}')
                sleep(2)
                continue
        except ValueError:
            print(f'{r}[!] Invalid input. Please enter a number.{n}')
            sleep(2)
            continue

        phone = str(accs[index][0])
        session_file = f'sessions/{phone}.session' # Ensure correct path
        
        # Remove session file
        if os.path.exists(session_file):
            if os.name == 'nt':
                os.system(f'del "{session_file}"')
            else:
                os.system(f'rm "{session_file}"')
            print(f'{lg}[i] Session file deleted: {session_file}{n}')
        else:
            print(f'{ye}[!] Session file not found (already deleted?): {session_file}{n}')

        del accs[index]
        with open('vars.txt', 'wb') as f:
            for account in accs:
                pickle.dump(account, f)
            print(f'\n{lg}[+] Account {phone} Deleted from vars.txt{n}')
            input(f'\nPress enter to goto main menu...')

    elif a == 4:
        # thanks to github.com/th3unkn0n for the snippet below
        print(f'\n{lg}[i] Checking for updates...')
        try:
           #  https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/version.txt
            version = requests.get('https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/version.txt')
            version.raise_for_status() # Check for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f'{r} Error checking for updates: {e}')
            print(f'{r} Please check your internet connection and retry')
            sleep(3)
            continue
            
        if float(version.text) > 2.0:
            prompt = str(input(f'{lg}[~] Update available[Version {version.text}]. Download?[y/n]: {r}'))
            if prompt.lower() in {'y', 'yes'}:
                print(f'{lg}[i] Downloading updates...')
                try:
                    # Download add.py
                    add_py = requests.get('https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/add.py')
                    add_py.raise_for_status()
                    with open('add.py', 'w', encoding='utf-8') as f:
                        f.write(add_py.text)
                    
                    # Download manager.py
                    manager_py = requests.get('https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/manager.py')
                    manager_py.raise_for_status()
                    with open('manager.py', 'w', encoding='utf-8') as f:
                        f.write(manager_py.text)
                        
                    print(f'{lg}[*] Updated to version: {version.text}')
                    print(f'{lg}[i] Please restart the script.')
                    input('Press enter to exit...')
                    exit()
                except requests.exceptions.RequestException as e:
                    print(f'{r}[!] Failed to download updates: {e}{n}')
                    input('Press enter to goto main menu...')
            else:
                print(f'{lg}[!] Update aborted.')
                input('Press enter to goto main menu...')
        else:
            print(f'{lg}[i] Your Telegram-Members-Adder is already up to date')
            input('Press enter to goto main menu...')

    elif a == 5:
        accs = []
        try:
            with open('vars.txt', 'rb') as f:
                while True:
                    try:
                        accs.append(pickle.load(f))
                    except EOFError:
                        break
        except FileNotFoundError:
            print(f'{r}[!] vars.txt not found. No accounts to display.{n}')
            sleep(3)
            continue
            
        if not accs:
            print(f'{r}[!] No accounts found in vars.txt.{n}')
            sleep(3)
            continue

        print(f'\n{cy}')
        print(f'\tList Of Phone Numbers Are')
        print('==========================================================')
        for i, z in enumerate(accs):
            print(f'\t[{i}] {z[0]}')
        print('==========================================================')
        print(f'\n{lg}Total accounts: {len(accs)}{n}')
        input('\nPress enter to goto main menu')

    elif a == 6:
        clr()
        banner()
        print(f'{lg}Goodbye!{n}')
        exit()
    
    else:
        print(f'{r}[!] Invalid choice. Please select from 1-6.{n}')
        sleep(2)
        
