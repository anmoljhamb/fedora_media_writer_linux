from DownloadISO import downloadISO
from VerifyHash import verifyHash 
from BurnUSB import burnUSB
from functions import take_input, breakline, get_choice, clrscr

def main():
    breakline()
    print('FEDORA MEDIA WRITER FOR LINUX')
    breakline()

    options = ['Download ISO', 'Use Local iso']

    FILE = None 

    if take_input(options) == options[0]:
        checksum, file = downloadISO().download()
        breakline()
        print('Verifing checksum...')       
        breakline()

        success = verifyHash().verify(checksum, file)
        assert success, "checksum doesn't match."
        FILE = file

    else:
        breakline()
        file = input('Enter the file\'s path: ')
        breakline()
        FILE = file 
    
    breakline()
    print('Buring iso To USB')
    breakline()

    burnUSB(file)

if __name__ == "__main__":
    main()