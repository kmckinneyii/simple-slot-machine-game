import random

while True:
    
    choice = input('Roll the dice? (yes/no): ').lower()
    if choice == 'yes':
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)
        total = dice1 + dice2
        print(f'You rolled a {dice1} and a {dice2}. Total = {total}.')
    
    elif choice == 'no':
        print('Game Exited.')
        break
    else:
        print('Invalid input. Please enter "yes" or "no".')
    
    