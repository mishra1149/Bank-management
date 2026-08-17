import json
import random
import string
from pathlib import Path




class BANK:
    database='data.json'
    data=[]
    try:
        if Path(database).exists():
            with open(database) as fs:
                data=json.loads(fs.read())
        else:
            print('no such file exist')
    except Exception as err:
        print(f'an exception occured as {err}')

    @classmethod
    def __update(cls):
        with open (cls.database,'w') as fs:
            fs.write(json.dumps(BANK.data))
    @classmethod
    def __accountgenerate(cls):
        alpha=random.choices(string.ascii_letters,k=3)
        num=random.choices(string.digits,k=2)
        spchar=random.choices('!@#$%^&*',k=1)
        id=alpha+num+spchar
        random.shuffle(id)
        return "".join(id)


                                 
    def createaccount(self):
        info = {
            "name":input ('enter your name'),
            "age":int (input('enter your age')),
            "email":input ('enter your email'),
            "pin":int (input('enter your 4 number pin')),
            "accountNo." : BANK.__accountgenerate(),
            "balance": 0
        }
        if info['age']<18 or len(str(info['pin']))!=4:
            print('sorry you cannot create your account')
        else:
            print('account has been created successfully')
            for i in info:
                print(f'{i}:{info[i]}')
            print('please note down your account number')
            BANK.data.append(info)
            BANK.__update()

    def depositmoney(self):
        accnumber=input('tell your account number')
        pin=int(input('tell your pin'))
        userdata=[i for i in BANK.data if i['accountNo.']==accnumber and i ['pin']==pin]
        if userdata ==False:
            print('sorry no data found')
        else:
            amount=int(input('how much you want to deposit'))
            if amount>10000 or amount<0:
                print('sorry the amount is too much you can deposit below 10000 or above 0')
            else:
                userdata[0]['balance'] +=amount
                BANK.__update()
                print('Amount deposit successfully')        



    def withdrawmoney(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))

        userdata = [i for i in BANK.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("soory no data found")
        
        else:
            amount = int(input("how much you want to withdraw "))
            if userdata[0]['balance']  < amount:
                print("soory you dont have that much money")
              
            else:
                
                userdata[0]['balance'] -= amount
                BANK.__update()
                print("Amount withdrow successfully ")

    def showdetails(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))
        
        userdata = [i for i in BANK.data if i['accountNo.'] == accnumber and i['pin'] == pin]
        print('your information are \n\n\n')
        for i in userdata[0]:
            print(f'{i}:{userdata[0][i]}')

    def updatedetails(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))
                
        userdata = [i for i in BANK.data if i['accountNo.'] == accnumber and i['pin'] == pin]
        if userdata==False:
            print('no such user found')
        else:
            print('you cannot change the age,pin,balance')
            print('fill the details for change or leave it empty if no change') 

            newdata={
                'name':input('enter your new name or press enter for skip'),
                'email':input('enter your new email or press enter for skip'),
                'pin':input('enter your new pin or press enter for skip')

            }  
            if newdata['name']=="":
                newdata['name']=userdata[0]['name']
            if newdata['email']=="":
                newdata['email']=userdata[0]['email']
            if newdata['pin']=="":
                newdata['pin']=userdata[0]['pin']

            newdata['age'] = userdata[0]['age']

            newdata['accountNo.'] = userdata[0]['accountNo.']
            newdata['balance'] = userdata[0]['balance']
            if type(newdata['pin'])==str:
                newdata['pin']=int(newdata['pin'])
            for i in newdata:
                 if newdata[i] == userdata[0][i]:
                     continue
                 else:
                     userdata[0][i] = newdata[i]

            BANK.__update()
            print("details updated successfully")

    def deleteuser(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))

        userdata = [i for i in BANK.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("sorry no such data exist ")
        else:
            index = BANK.data.index(userdata[0])
            BANK.data.pop(index)
            print("account deleted successfully ")
            BANK.__update()    

                   


                        
user=BANK()
print('press 1 for create an account')
print('press 2 for deposit money')
print('press 3 for withdrawl money')
print('press 4 for details')
print('press 5 for update details')
print('press 6 for delete an account')

check=int(input('enter your response'))
if check==1:
    user.createaccount()

if check==2:
    user.depositmoney()   

if check==3:
    user.withdrawmoney()

if check==4:
    user.showdetails()    

if check==5:
    user.updatedetails()    

if check==6:
    user.deleteuser()