'''
================SAIFALISEW1508=====================
Telegram members adding script
Coded by a kid- github.com/saifalisew1508
Apologies if anything in the code is dumb :)
Copy with credits
************************************************
'''


# import libraries
import asyncio
import sys
import os
import pickle
import time
import random
from colorama import init, Fore

from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel, UserStatusRecently, UserStatusOnline, UserStatusOffline
from telethon.errors.rpcerrorlist import (
    PeerFloodError, UserPrivacyRestrictedError, PhoneNumberBannedError, ChatAdminRequiredError,
    ChatWriteForbiddenError, UserBannedInChannelError, UserAlreadyParticipantError, FloodWaitError
)
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, AddChatUserRequest


init()


r = Fore.RED
lg = Fore.GREEN
rs = Fore.RESET
w = Fore.WHITE
grey = '\033[97m'
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [r, lg, w, ye, cy]
info = f'{lg}[{w}i{lg}]{rs}'
error = f'{lg}[{r}!{lg}]{rs}'
success = f'{w}[{lg}*{w}]{rs} '
INPUT = f'{lg}[{cy}~{lg}]{rs} '
plus = f'{w}[{lg}+{w}]{rs} '
minus = f'{w}[{lg}-{w}]{rs} '

# Hardcoded API ID and Hash from the original script
API_ID = 3910389
API_HASH = '86f861352f0ab76a251866059a6adbd6'

def banner():
    # fancy logo
    b = [
    '░█████╗░██████╗░██████╗░███████╗██████╗░',
    '██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗',
    '███████║██║░░██║██║░░██║█████╗░░██████╔╝',
    '██╔══██║██║░░██║██║░░██║██╔══╝░░██╔══██╗',
    '██║░░██║██████╔╝██████╔╝███████╗██║░░██║',
    '╚═╝░░╚═╝╚═════╝░╚═════╝░╚══════╝╚═╝░░╚═╝'
    ]
    for char in b:
        print(f'{random.choice(colors)}{char}{rs}')
    print('This is a demo version of my premium software, provided for trial purposes only. To access the full features and original licensed version, please contact me directly through the addresses below. The demo may have limited functionality and is not intended for long-term use if you are interested in purchasing the complete version, reach out and I will guide you through the process.')
    print('I am not responsible for your account got banned due to using this software as i said this is demo tool its mean its a feature less software test software to show users how its works.')

    print(f'{lg}Version: {w}2.9.1.0 (Async Update){lg} | GitHub: {w}@saifalisew1508{rs}')
    print(f'{lg}Telegram: {w}@DearSaif{lg} | Instagram: {w}@saifali_patho{rs}')


# function to clear screen
def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# func to log scraping details
def log_status(scraped, index):
    with open('status.dat', 'wb') as f:
        pickle.dump([scraped, int(index)], f)
    print(f'{info}{lg} Session stored in {w}status.dat{lg}')
    

def exit_window():
    input(f'\n{cy} Press enter to exit...')
    clr()
    banner()
    sys.exit()

# Async function to check for banned accounts
async def check_accounts(accounts):
    print('\n' + info + lg + ' Checking for banned accounts...' + rs)
    banned_accounts = []
    workable_accounts = []
    
    for acc in accounts:
        phn = acc[0]
        print(f'{plus}{grey} Checking {lg}{phn}')
        clnt = TelegramClient(f'sessions/{phn}', API_ID, API_HASH)
        
        try:
            await clnt.connect()
            if not await clnt.is_user_authorized():
                try:
                    await clnt.send_code_request(phn)
                    print(f'{info} {lg}Sent code to {w}{phn}{lg} (Just checking ban status, not logging in)')
                except PhoneNumberBannedError:
                    print(f'{error} {w}{phn} {r}is banned!{rs}')
                    banned_accounts.append(acc)
                except Exception as e:
                    print(f'{error} {w}{phn} {r}Error: {e}{rs}')
                    # Could be other issues, but we'll treat it as non-workable for now
            else:
                print(f'{success}{lg}{phn} is active.')
                workable_accounts.append(acc)
        
        except Exception as e:
            print(f'{error} {w}{phn} {r}Failed to connect: {e}{rs}')
            # Could be network or other issue, skip this account
            
        finally:
            if clnt.is_connected():
                await clnt.disconnect()
            await asyncio.sleep(0.5)

    # Remove banned accounts from the main list
    final_accounts = [acc for acc in accounts if acc not in banned_accounts]
    
    if banned_accounts:
        print(f'{info}{lg} Banned accounts removed [Remove permanently using manager.py]{rs}')
    
    return final_accounts

async def main():
    # Load accounts from vars.txt
    try:
        accounts = []
        with open('vars.txt', 'rb') as f:
            while True:
                try:
                    accounts.append(pickle.load(f))
                except EOFError:
                    break
    except FileNotFoundError:
        print(f'{error}{r} File "vars.txt" not found. Please run manager.py to add accounts.{rs}')
        exit_window()

    if not accounts:
        print(f'{error}{r} No accounts found in "vars.txt". Please run manager.py to add accounts.{rs}')
        exit_window()

    # Check accounts asynchronously
    accounts = await check_accounts(accounts)
    
    if not accounts:
        print(f'{error}{r} All accounts are banned or unusable. Exiting.{rs}')
        exit_window()

    print(f'\n{info} Sessions checked!')
    await asyncio.sleep(1)
    clr()
    banner()

    # read user details
    index = 0
    scraped_grp = ''
    try:
        # request to resume adding
        with open('status.dat', 'rb') as f:
            status = pickle.load(f)
            scraped_grp = status[0]
            index = int(status[1])
        
        lol = input(f'{INPUT}{cy} Resume scraping members from {w}{status[0]}{lg}? [y/n]: {r}')
        if 'y' not in lol.lower():
            if os.name == 'nt': 
                os.system('del status.dat')
            else: 
                os.system('rm status.dat')
            scraped_grp = input(f'{INPUT}{cy} Public/Private group url link to scrape members: {r}')
            index = 0
    except FileNotFoundError:
        scraped_grp = input(f'{INPUT}{cy} Public/Private group url link to scrape members: {r}')
        index = 0

    print(f'{info}{lg} Total accounts: {w}{len(accounts)}')
    number_of_accs = int(input(f'{INPUT}{cy} How Many Accounts You Want Use In Adding: {r}'))
    
    if number_of_accs > len(accounts):
        print(f'{error}{r} Only {lg}{len(accounts)}{r} accounts available. Using all of them.')
        number_of_accs = len(accounts)
        
    print(f'{info}{cy} Choose an option{lg}')
    print(f'{cy}[0]{lg} Add to public group')
    print(f'{cy}[1]{lg} Add to private group')
    choice = int(input(f'{INPUT}{cy} Enter choice: {r}'))
    
    if choice == 0:
        target = str(input(f'{INPUT}{cy} Enter public group url link: {r}'))
    else:
        target = str(input(f'{INPUT}{cy} Enter private group url link: {r}'))
        
    print(f'{grey}_'*50)
    status_choice = str(input(f'{INPUT}{cy} Do you wanna add active members (recently or online)?[y/n]: {r}'))
    
    to_use = list(accounts[:number_of_accs])
    # This logic re-orders the file to put used accounts at the end
    remaining_accounts = list(accounts[number_of_accs:])
    with open('vars.txt', 'wb') as f:
        for a in remaining_accounts:
            pickle.dump(a, f)
        for ab in to_use:
            pickle.dump(ab, f)

    sleep_time = int(input(f'{INPUT}{cy} Enter delay time per request{w}[{lg}i suggest 30-60s{w}]: {r}'))
    print(f'{grey}-'*50)
    print(f'{success}{lg} -- Adding members from {w}{len(to_use)}{lg} account(s) --')

    total_added_count = 0
    
    for acc in to_use:
        stop_count = 0  # Local counter for this account, to add ~60 members
        peer_flood_status = 0
        
        c = TelegramClient(f'sessions/{acc[0]}', API_ID, API_HASH)
        
        print(f'{plus}{grey} User: {cy}{acc[0]}{lg} -- {cy}Starting session... ')
        
        try:
            await c.start(acc[0])
            acc_name = (await c.get_me()).first_name
            print(f'{success}{grey} User: {cy}{acc_name}{lg} -- Session started.')

            # --- Join Source Group ---
            try:
                if '/joinchat/' in scraped_grp:
                    g_hash = scraped_grp.split('/joinchat/')[1]
                    await c(ImportChatInviteRequest(g_hash))
                else:
                    await c(JoinChannelRequest(scraped_grp))
                print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to scrape')
            except UserAlreadyParticipantError:
                print(f'{info}{grey} User: {cy}{acc_name}{lg} -- Already in scrape group')
            
            scraped_grp_entity = await c.get_entity(scraped_grp)

            # --- Join Target Group ---
            if choice == 0: # Public
                try:
                    await c(JoinChannelRequest(target))
                    print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to add')
                except UserAlreadyParticipantError:
                    print(f'{info}{grey} User: {cy}{acc_name}{lg} -- Already in target group')
                target_entity = await c.get_entity(target)
                target_details = InputPeerChannel(target_entity.id, target_entity.access_hash)
            else: # Private
                try:
                    grp_hash = target.split('/joinchat/')[1]
                    await c(ImportChatInviteRequest(grp_hash))
                    print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- Joined group to add')
                except UserAlreadyParticipantError:
                    print(f'{info}{grey} User: {cy}{acc_name}{lg} -- Already in target group')
                target_entity = await c.get_entity(target)
                target_details = target_entity

        except Exception as e:
            print(f'{error}{r} User: {cy}{acc_name}{lg} -- Failed to join group(s)')
            print(f'{error} {r}{e}')
            continue # Move to next account
            
        print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- {cy}Retrieving entities...')
        await c.get_dialogs() # Populate entity cache
        
        try:
            # Get total member count
            total_members = (await c.get_participants(scraped_grp_entity, limit=0)).total
            print(f'{info}{lg} Total members in scrape group: {w}{total_members}')
        except Exception as e:
            print(f'{error}{r} Couldn\'t scrape members')
            print(f'{error}{r} {e}')
            continue

        if index >= total_members:
            print(f'{error}{lg} No new members to add!')
            continue

        print(f'{info}{lg} Starting from index: {w}{index}')

        # Use iter_participants with offset for efficient resuming
        async for user in c.iter_participants(scraped_grp_entity, offset=index):
            
            # Check if this account has reached its 60-user limit
            if stop_count >= 60:
                print(f'{info}{grey} User: {cy}{acc_name}{lg} -- Reached 60 users limit for this session.')
                break
            
            # Check if this account is getting too many PeerFloodErrors
            if peer_flood_status >= 10:
                print(f'{error}{r} Too many Peer Flood Errors for {cy}{acc_name}{lg}! Switching account...')
                break

            try:
                if user.bot:
                    print(f'{minus}{grey} Skipping Bot: {cy}{user.first_name}')
                    index += 1
                    continue
                
                # Active member filter
                if 'y' in status_choice.lower():
                    if not (isinstance(user.status, (UserStatusOnline, UserStatusRecently))):
                        print(f'{minus}{grey} Skipping Inactive User: {cy}{user.first_name}')
                        index += 1
                        continue

                # Add user
                if choice == 0: # Public
                    await c(InviteToChannelRequest(target_details, [user]))
                else: # Private
                    await c(AddChatUserRequest(target_details.id, user, 42)) # fwd_limit = 42
                
                user_id = user.first_name
                target_title = target_entity.title
                print(f'{plus}{grey} User: {cy}{acc_name}{lg} -- {cy}{user_id} {lg}--> {cy}{target_title}')
                
                total_added_count += 1
                stop_count += 1
                
                print(f'{info}{grey} User: {cy}{acc_name}{lg} -- Sleep {w}{sleep_time} {lg}second(s)')
                await asyncio.sleep(sleep_time)

            except UserPrivacyRestrictedError:
                print(f'{minus}{grey} User: {cy}{acc_name}{lg} -- {r}User Privacy Restricted')
            except PeerFloodError:
                print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Peer Flood Error.')
                peer_flood_status += 1
                # Don't increment index, retry this user with next account
                break # Break from this account's loop
            except ChatWriteForbiddenError:
                print(f'{error}{r} Can\'t add to group. Contact group admin to enable members adding')
                log_status(scraped_grp, index)
                exit_window()
            except UserBannedInChannelError:
                print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Banned from writing in groups')
                break # This account is useless, move to next
            except ChatAdminRequiredError:
                print(f'{error}{grey} User: {cy}{acc_name}{lg} -- {r}Chat Admin rights needed to add')
                break # This account can't add, move to next
            except UserAlreadyParticipantError:
                print(f'{minus}{grey} User: {cy}{acc_name}{lg} -- {r}User is already a participant')
            except FloodWaitError as e:
                print(f'{error}{r} Flood Wait Error: {e.seconds}s')
                # Don't increment index, retry this user with next account
                break # Break from this account's loop
            except ValueError:
                print(f'{error}{r} Error in Entity (likely scraped a deleted account)')
            except KeyboardInterrupt:
                print(f'{error}{r} ---- Adding Terminated ----')
                log_status(scraped_grp, index)
                exit_window()
            except Exception as e:
                print(f'{error} {e}')
            
            # Increment global index *after* processing a user (success or skip)
            index += 1

        # Disconnect client after it's done or hits an error
        await c.disconnect()
        print(f'{info}{grey} User: {cy}{acc_name}{lg} -- Session closed.')

    if total_added_count != 0:
        print(f"\n{success}{lg} Adding session ended. Total members added: {w}{total_added_count}")
    else:
        print(f"\n{info}{lg} Adding session ended. No new members added.")

    try:
        log_status(scraped_grp, index)
    except:
        pass
    
    exit_window()


if __name__ == "__main__":
    clr()
    banner()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f'\n{error}{r} Exiting...')
        clr()
        banner()
        sys.exit()
        
