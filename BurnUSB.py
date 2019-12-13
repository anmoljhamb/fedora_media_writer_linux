import time 
import re
import subprocess as sp 
import os, stat, shlex, sys
from functions import take_input, breakline, get_choice, clrscr


def get_current_partition():
    '''
    Gets the current working partition of the system. i.e the partition on which the system is booted on.
    '''
    out = sp.Popen(shlex.split("df /"), stdout=sp.PIPE).communicate()
    m=re.search(r'(/[^\s]+)\s',str(out))
    if m:
        return m.group(1)
    return False

def get_usb():
    output = sp.check_output(['sudo fdisk -l'], shell=True)    
    output = output.decode('utf8')
    Lines = output.split('\n')
    usbs = []
    for line in Lines:
        if re.search(r'/dev/sd.:', line):
            usbs.append(line)
    curr_partition = get_current_partition()
    #Filtering usbs
    usbs = [usb for usb in usbs if usb.split()[1].strip(':') not in curr_partition]
    assert len(usbs) > 0, "No usb found."
    return usbs

class burnUSB:
    def __init__(self, iso_path):

        assert os.path.isfile(iso_path), "Invalid Path for ISO file."

        choice = take_input(get_usb())
        usb = choice.split()[1].strip(':')
        breakline()
        print('Are you sure you want to continue? This will destroy the data in pendrive.')
        print('1) For continuing\n2) For Exiting.')
        choice = get_choice()
        
        assert choice.isdigit() and int(choice) in range(1, 3), "Invalid Choice."

        if choice == '2':
            print('Exiting the program.')
            time.sleep(2)
            sp.call(['clear'], shell=True)
            exit()

        print(f'UNMOUNTING {usb}')
        breakline()
        success = sp.call([f'umount {usb}*'], shell=True)
        breakline()

        print('Does your system support efi?')
        choice = take_input(['Yes', 'No'])
        
        if choice == 'Yes':
            print('Formatting the drive in fat32')
            success = sp.call([f'mkfs.vfat {usb}'], shell=True)
        
        else:
            print('Formatting the drive in ext4')
            success = sp.call([f'mkfs.ext4 {usb}'], shell=True)
        
        
        print(f"Burning {iso_path} to {usb}")
        success = sp.call([f'dd status="progress" if="{iso_path}" of={usb}'], shell=True)


def main():
    burnUSB('sample.iso')

if __name__ == "__main__":
    main()
