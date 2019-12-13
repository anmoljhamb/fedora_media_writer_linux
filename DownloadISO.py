import requests
from bs4 import BeautifulSoup
import os 
import subprocess as sp
import wget
from functions import take_input, breakline, get_choice, clrscr

class downloadISO:
    def download(self):
        self.pprint(lambda: print("Getting Latest Fedora Version."))
        base_url = "https://dl.fedoraproject.org/pub/fedora/linux/releases"
        soup = self.get_soup(base_url)
        Links = self.get_links(soup)
        Versions = []
        for link in Links:
            link = link.text.strip('/')
            if link.isdigit():
                Versions.append(int(link))
        print(f'The latest version is {max(Versions)}')
        breakline()

        choice = take_input(['Workstation', 'Spins'])
        base_url += f'/{max(Versions)}/{choice}/x86_64/iso'

        soup = self.get_soup(base_url)
        Links = self.get_links(soup)

        ISOs = [link.text for link in Links if '.iso' in link.get('href')]

        CHECKSUM = None
        for link in Links:
            if 'CHECKSUM' in link.text:
                CHECKSUM = link.text 

        self.pprint(lambda: print('The available ISOs: '))
        choice = take_input(ISOs)
        
        if not CHECKSUM:
            print('No checksum found, do you still want to proceed?')
            choice = take_input(['Yes.', 'No.'])
            if choice == 2:
                exit()

        wget.download(base_url+'/'+choice, choice)
        if CHECKSUM:
            print('Downloading checksum')
            wget.download(CHECKSUM, 'checksum')
            CHECKSUM = 'checksum.txt'

        return CHECKSUM, choice 

    def pprint(self, func):
        breakline()
        func()
        breakline()

    def get_links(self, soup):
        return soup.findAll('a')
    
    def get_soup(self, url):
        return BeautifulSoup(requests.get(url).content, "lxml")



def main():
    downloadISO().download()

if __name__ == "__main__":
    main()