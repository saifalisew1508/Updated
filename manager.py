#!/usr/bin/env python3
# manager_1_42.py — cleaned synchronous version for Telethon v1.42.x

import os
import pickle
import asyncio
from pathlib import Path
from time import sleep

from colorama import init as colorama_init, Fore

# Telethon v1 (sync helper kept)
from telethon.sync import TelegramClient
from telethon.errors import PhoneNumberBannedError

# Optional; we'll import requests safely
try:
    import requests
except ImportError:
    print("Installing requests (missing).")
    os.system("pip install requests")
    import requests

colorama_init(autoreset=True)

# Colors
n = Fore.RESET
lg = Fore.LIGHTGREEN_EX
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [lg, r, w, cy, ye]

# Config — replace these if they're sensitive
API_ID = 3910389
API_HASH = "86f861352f0ab76a251866059a6adbd6"

SESSIONS_DIR = Path("sessions")
VARS_FILE = Path("vars.txt")
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def banner():
    import random
    b = [
        "░██████╗███████╗████████╗██╗░░░██╗██████╗░",
        "██╔════╝██╔════╝╚══██╔══╝██║░░░██║██╔══██╗",
        "╚█████╗░█████╗░░░░░██║░░░██║░░░██║██████╔╝",
        "░╚═══██╗██╔══╝░░░░░██║░░░██║░░░██║██╔═══╝░",
        "██████╔╝███████╗░░░██║░░░╚██████╔╝██║░░░░░",
        "╚═════╝░╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░░░",
    ]
    for line in b:
        print(f"{colors[0]}{line}{n}")
    print("Contact below address for get premium script")
    print(f"{lg}Version: {w}2.6.82{lg} | GitHub: {w}@saifalisew1508{n}")
    print(f"{lg}Telegram: {w}@DearSaif{lg} | Instagram: {w}www.instagram.com/saifaliopp{n}")


def clr():
    os.system("cls" if os.name == "nt" else "clear")


def ensure_vars_file():
    if not VARS_FILE.exists():
        VARS_FILE.touch()


def read_all_accounts():
    accounts = []
    if not VARS_FILE.exists():
        return accounts
    with VARS_FILE.open("rb") as f:
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break
    return accounts


def write_all_accounts(accounts):
    with VARS_FILE.open("wb") as f:
        for a in accounts:
            pickle.dump(a, f)


def sanitize_phone(s: str) -> str:
    return "".join(s.split())


def add_new_accounts():
    ensure_vars_file()
    new_accs = []
    try:
        number_to_add = int(input(f"\n{lg} [~] Enter How Many Accounts You Want To Add: {r}"))
    except ValueError:
        print(f"{r}Invalid number{n}")
        sleep(1.5)
        return

    with VARS_FILE.open("ab") as g:
        for _ in range(number_to_add):
            phone_number = input(f"\n{lg} [~] Enter Phone Number With Country Code: {r}")
            parsed_number = sanitize_phone(phone_number)
            pickle.dump([parsed_number], g)
            new_accs.append(parsed_number)
    print(f"\n{lg} [i] Saved all accounts in {VARS_FILE}{n}")

    # Attempt login for each new account using sync .start()
    for number in new_accs:
        client = TelegramClient(str(SESSIONS_DIR / number), API_ID, API_HASH)
        try:
            client.start(phone=number)
            print(f"{lg}[+] Login successful: {number}{n}")
        except Exception as e:
            print(f"{r}[-] Failed to login {number}: {e}{n}")
        finally:
            try:
                client.disconnect()
            except Exception:
                pass

    input("\n Press enter to goto main menu...")


def filter_banned_accounts():
    accounts = read_all_accounts()
    if not accounts:
        print(f"{r}[!] There are no accounts! Please add some and retry")
        sleep(2)
        return

    banned_accs = []
    for account in accounts:
        phone = str(account[0])
        client = TelegramClient(str(SESSIONS_DIR / phone), API_ID, API_HASH)
        try:
            client.connect()
            if not client.is_user_authorized():
                try:
                    client.send_code_request(phone)
                    print(f"{lg}[+] {phone} is not banned{n}")
                except PhoneNumberBannedError:
                    print(f"{r}{phone} is banned!{n}")
                    banned_accs.append(account)
                except Exception as exc:
                    print(f"{ye}[-] Could not verify {phone}: {exc}{n}")
            else:
                print(f"{lg}[+] {phone} already authorized locally{n}")
        finally:
            try:
                client.disconnect()
            except Exception:
                pass

    if banned_accs:
        remaining = [a for a in accounts if a not in banned_accs]
        write_all_accounts(remaining)
        print(f"{lg}[i] Removed {len(banned_accs)} banned account(s){n}")
    else:
        print(f"{lg}Congrats! No banned accounts{n}")

    input("\nPress enter to goto main menu...")


def delete_specific_account():
    accs = read_all_accounts()
    if not accs:
        print(f"{r}[!] There are no accounts to delete.")
        sleep(1.2)
        return
    print(f"{lg}[i] Choose an account to delete\n")
    for i, acc in enumerate(accs):
        print(f"{lg}[{i}] {acc[0]}{n}")
    try:
        index = int(input(f"\n{lg}[+] Enter a choice: {n}"))
        phone = str(accs[index][0])
    except (ValueError, IndexError):
        print(f"{r}Invalid choice{n}")
        sleep(1.2)
        return

    # Remove potential session files for that phone (v1 uses .session)
    possible = [
        SESSIONS_DIR / phone,
        SESSIONS_DIR / f"{phone}.session",
        SESSIONS_DIR / f"{phone}.session-journal",
    ]
    for p in possible:
        try:
            if p.exists():
                p.unlink()
        except Exception:
            pass

    del accs[index]
    write_all_accounts(accs)
    print(f"\n{lg}[+] Account Deleted{n}")
    input(f"\nPress enter to goto main menu...")


def update_script():
    print(f"\n{lg}[i] Checking for updates...")
    try:
        r = requests.get("https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/version.txt", timeout=10)
        r.raise_for_status()
    except Exception:
        print(f"{r} You are not connected to the internet or URL unreachable{n}")
        input("Press enter to goto main menu...")
        return
    try:
        remote_v = float(r.text.strip())
    except Exception:
        print(f"{r} Invalid remote version response{n}")
        input("Press enter to goto main menu...")
        return

    if remote_v > 2.0:
        prompt = input(f"{lg}[~] Update available[Version {r.text.strip()}]. Download?[y/n]: {r}").lower()
        if prompt in {"y", "yes"}:
            print(f"{lg}[i] Downloading updates...")
            base = "https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/"
            for name in ("add.py", "manager.py"):
                try:
                    rr = requests.get(base + name, timeout=15)
                    rr.raise_for_status()
                    with open(name, "wb") as f:
                        f.write(rr.content)
                    print(f"{lg}[*] Updated {name}{n}")
                except Exception as e:
                    print(f"{r} Failed to update {name}: {e}{n}")
            input("Press enter to exit...")
            exit(0)
        else:
            print(f"{lg}[!] Update aborted.")
            input("Press enter to goto main menu...")
    else:
        print(f"{lg}[i] Your Telegram-Members-Adder is already up to date")
        input("Press enter to goto main menu...")


def display_all_accounts():
    accs = read_all_accounts()
    print(f"\n{cy}")
    print(f"\tList Of Phone Numbers Are")
    print("==========================================================")
    for z in accs:
        print(f"\t{z[0]}")
    print("==========================================================")
    input("\nPress enter to goto main menu")


def main():
    ensure_vars_file()
    while True:
        clr()
        banner()
        print(f"{lg}[1] Add new accounts{n}")
        print(f"{lg}[2] Filter all banned accounts{n}")
        print(f"{lg}[3] Delete specific accounts{n}")
        print(f"{lg}[4] Update your Script{n}")
        print(f"{lg}[5] Display All Accounts{n}")
        print(f"{lg}[6] Quit{n}")
        try:
            a = int(input("\nEnter your choice: "))
        except ValueError:
            print(f"{r}Invalid choice{n}")
            sleep(1.2)
            continue

        if a == 1:
            add_new_accounts()
        elif a == 2:
            filter_banned_accounts()
        elif a == 3:
            delete_specific_account()
        elif a == 4:
            update_script()
        elif a == 5:
            display_all_accounts()
        elif a == 6:
            clr()
            banner()
            exit(0)
        else:
            print(f"{r}Invalid option{n}")
            sleep(1.2)


if __name__ == "__main__":
    main()
