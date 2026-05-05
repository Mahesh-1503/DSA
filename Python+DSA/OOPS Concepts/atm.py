class AtmMachine:
    def __init__(self):
        print(id(self))
        self.pin = ''
        self.balance = 0
        self.menu()

    def menu(self):
        while True:
            user_input = input('''
Hi how can I help you?
1. Press 1 to create pin
2. Press 2 to change pin
3. Press 3 to check balance
4. Press 4 to withdraw
5. Press 5 to deposit
6. Press anything else to exit
''')

            if user_input == '1':
                self.create_pin()
            elif user_input == '2':
                self.change_pin()
            elif user_input == '3':
                self.check_balance()
            elif user_input == '4':
                self.withdraw()
            elif user_input == '5':
                self.deposit()
            else:
                print("Thank you for using ATM!")
                break

    def create_pin(self):
        self.pin = int(input("Enter your pin: "))
        self.balance = int(input("Enter Balance: "))
        print("Pin Created Successfully!")

    def change_pin(self):
        old_pin = int(input('Enter your old pin: '))
        if old_pin == self.pin:
            new_pin = int(input('Enter your new pin: '))
            self.pin = new_pin
            print("Pin Changed Successfully!")
        else:
            print("Incorrect PIN!")

    def check_balance(self):
        user_pin = int(input("Enter your pin: "))
        if user_pin == self.pin:
            print(f"Your balance is: {self.balance}")
        else:
            print("Incorrect PIN!")

    def withdraw(self):
        user_pin = int(input("Enter your pin: "))
        if user_pin == self.pin:
            amount = int(input("Enter amount to withdraw: "))
            if amount <= self.balance:
                self.balance -= amount
                print(f"Withdrawn {amount}. Remaining balance: {self.balance}")
            else:
                print("Insufficient balance!")
        else:
            print("Incorrect PIN!")

    def deposit(self):
        user_pin = input("Enter your pin: ")
        if user_pin == self.pin:
            amount = int(input("Enter amount to deposit: "))
            self.balance += amount
            print(f"Deposited {amount}. New balance: {self.balance}")
        else:
            print("Incorrect PIN!")


# Run the ATM
SBI = AtmMachine()
# HDFC = AtmMachine()
print(id(SBI))
