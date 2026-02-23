# user_data = [i for i in data if i['Account.no']== account and i ['Pin']==pin]
# print(user_data)

# if user_data == False:
#     print('No such user')
# else:
#     balance = int(input('Enter balance :- '))
#     user_data[0]['Balance'] += balance
#     print(user_data)


# account = input("Enter Acc :- ")          # list comperehension 
# pin = int(input("Enter pin :- "))


# a = {'a':10,'b':20,'c'30}
# b = {'a': 'replaced', 'b': 'repalced'} 

# a["a"] = b['a']
# b[]
    
main_dict = [{"name": "Himanshu Malviya ", "age": 20, "Phonenumber": 7974646353, "Email": "himanshumalviya@gmail.com", "Pin": 2244, "Account.no": "I630AB4o", "Balance": 0}]
new_dict  = [{"name": "ankur", "age": 21, "Phonenumber": 700006353, "Email":"lviya@gmail.com", "Pin": 2233, "Account.no": "I630AB4o", "Balance": 0}]

main_dict['name'] = new_dict['name']
main_dict['age'] = new_dict['age']
main_dict['Pin'] = new_dict['Pin']
main_dict['Email'] = new_dict['Email']


print()
