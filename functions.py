import os

def get_choice():
    breakline()
    choice = input("Your choice: ")
    breakline()
    return choice

def breakline():
    print('-'*70)

def clrscr():
    os.system('clear')    

def take_input(List):
    '''
    A function to let the user choose some thing from a list.
    '''
    breakline()
    for i, elem in enumerate(List):
        print(f'{i+1}: {elem}')
    breakline()

    choice = get_choice()
    assert choice.isdigit() and int(choice) in range(1, len(List)+1)
    
    return List[int(choice)-1]