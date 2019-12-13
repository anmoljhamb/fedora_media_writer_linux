import subprocess as sp

class verifyHash:
    def verify(self, checksum_file, fedora_version):
        with open(checksum_file) as f:
            data = f.readlines()
        hash_name = data[1].split(': ')[1].lower()
        index = None 
        for i in range(2, len(data)):
            data[i] = data[i].strip('\n')
            if fedora_version in data[i]:
                index = i+1
                break 
        if not index:
            print('Couldn\'t find checksum of the give iso file')

        checksum = data[index].split(' = ')[1].strip('\n')
        output = sp.check_output([f'echo "{checksum} *{fedora_version}" | shasum -a 256 --check'], shell=True)
        if output.decode('utf8').split(': ')[1].strip('\n') == 'OK':
            return True
        return False

def main():
    print(verifyHash().verify('checksum', 'ubuntu-19.10-desktop-amd64.iso'))

if __name__ == "__main__":
    main()