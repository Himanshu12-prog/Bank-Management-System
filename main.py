from pathlib import Path
import json
import random
import string

class Bank:
    database = "data.json"
    data = []   # yeh data json main save hoga 

    try:
        if Path(database).exists():
            print("File exists")
            with open(database) as fs:
                data = json.loads(fs.read())                        
        else:
            print("No such file exists...")
    except Exception as err:
        print(f"Error Occured {err}")

    @classmethod
    def update(cls):
        with open(Bank.database,'w') as fs:
            fs.write(json.dumps(cls.data))

    @staticmethod
    def generateAcc():
        digits = random.choices(string.digits,k=4)
        alpha  = random.choices(string.ascii_letters,k=4)
        id = digits + alpha
        random.shuffle(id)
        return "".join(id)

    def CreateAccount(self):
        info = {
            'name' : input('Enter your name :- '),
            'age' : int(input('Enter your age :- ')),   
            'Phonenumber': int(input('Enter your number :- ')),
            'Email': input('Enter your Email :- '),
            'Pin' : int(input("Enter your pin :-")),
            'Account.no': Bank.__generateAcc(),
            'Balance' : 0
        }
        if info ['age'] > 18 and len(str(info['Pin'])) == 4 and len(str(info['Phonenumber'])) == 10 :      
            Bank.data.append(info)
            Bank.update()
            print('Data added in list')
            print(Bank.data)
        else:
            print('Credinitials are not valid!')
        
    def depositmoney(self):
        accountno = input("Enter your Account.no :- ")
        Pin = int(input("Enter your 4 digits pin :- "))

        user_data = [i for i in Bank.data if i["Account.no"]==accountno and i ['Pin']==Pin ]
        if user_data == False:
            print("User not Found")
        else:
            amount = int (input("Enter your amount :- "))
            if amount <= 0:
                print("Invalid Amount")
            elif amount > 10000:
                print("Greater than 10000")
            else:
                user_data[0]["Balance"] +=  amount
                Bank.__update()
                print("Amount Credited")

    def Withdrawmoney(self):
        accountno = input("Enter your Account.no :- ")
        Pin = int(input("Enter your 4 digits pin :- "))

        user_data = [i for i in Bank.data if i["Account.no"]==accountno and i ['Pin']==Pin ]
        if user_data == False:
            print("User not Found")
        else:
            amount = int (input("Enter your amount :- "))
            if amount <= 0:
                print("Invalid Amount")
            elif amount > 10000:
                print("Greater than 10000")
            else:
                if user_data[0]["Balance"] <  amount:
                    print("insufficent Funds.....")
                else:
                    user_data[0]["Balance"] -= amount    
                    Bank.update()
                    print("Amount debited")
    
    def Detalis(self):
        accountno = input("Enter your Account.no :- ")
        Pin = int(input("Enter your 4 digits pin :- "))

        user_data = [i for i in Bank.data if i["Account.no"]==accountno and i ['Pin']==Pin ]
        if user_data == False:
            print("User not Found")
        else:
            for i in user_data[0]:
                print(i,user_data[0][i])
    
    def update_detalis(self):
        accountno = input("Enter your Account.no :- ")
        Pin = int(input("Enter your 4 digits pin :- "))

        user_data = [i for i in Bank.data if i["Account.no"]==accountno and i ['Pin']==Pin ]
        if user_data == False:
            print("User not Found")
        else:
            print("You cannot change your Account.no and Balance")

            print("Enter Your details to update or just press enter to skip them")

            new_data = { 
                'name' : input('Enter your name :- '),
                'age' : input('Enter your age :- '),   
                'Phonenumber': input('Enter your number :- '),
                'Email': input('Enter your Email :- '),
                'Pin' : input("Enter your pin :-"),
            }

            if new_data['name'] == "":
                new_data['name'] == user_data[0]['name']
            
            if new_data['age'] == "":
                new_data['age'] == user_data[0]['age']
            else:
                new_data['age'] == int(new_data['age'])
            
            if new_data['Phonenumber'] == "":
                new_data['Phonenumber'] == user_data[0]['Phonenumber']
            else:
                new_data['Phonenumber'] == int(new_data['Phonenumber'])
            
            if new_data['Email'] == "":
                new_data['Email'] == user_data[0]['Email']

            if new_data['Pin'] == "":
                new_data['Pin'] == user_data[0]['Pin']
            else:
                new_data['Pin'] == int(new_data['Pin'])

            new_data['Account.no'] = user_data[0]['Account.no']
            new_data['Balance'] = user_data[0]['Balance']

            user_data[0].update(new_data)
            Bank.__update()

            # if new_data['Phonenumber'] == "":
            #     new_data['Phonenumber'] == user_data[0]['Phonenumber']
            # else:
            #     new_data['Phonenumber'] == int(new_data['Phonenumber'])

    def delete(self):
        accountno = input("Enter your Account.no :- ")
        Pin = int(input("Enter your 4 digits pin :- "))

        user_data = [i for i in Bank.data if i["Account.no"]==accountno and i ['Pin']==Pin ]
        if user_data == False:
            print("User not Found")
        else:
            print("Are you sure to delete your account ? (Yes/No)")
            choice =  input()
            if choice == "Yes":
                ind = Bank.data.index(user_data[0])
                Bank.data.pop(ind)
                Bank.__update()
                print("Account deleted successfully")
            else:
                print("Operation Termineted")


obj = Bank()
print("Press 1 to creating account")
print("Press 2 to Depositing money")
print("Press 3 to Withdraw money")
print("Press 4 to account Details")
print("Press 5 to updating account details")
print("Press 6 to Deleting account")
choice = int(input("enter your choice :- "))
if choice == 1:
    obj.CreateAccount()
elif choice == 2 :
    obj.depositmoney()
elif choice == 3:
    obj.Withdrawmoney()
elif choice == 4:
    obj.Detalis()
elif choice == 5:
    obj.update_detalis()
elif choice == 6:
    obj.delete()




# obj.CreateAccount()
# obj.depositmoney()
# obj.Withdrawmoney()
# obj.Detalis()