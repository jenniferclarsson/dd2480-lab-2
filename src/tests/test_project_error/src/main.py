''' 
FAULTY PYTHON PROGRAM 
Expects Pylint to throw a "no-member / E1101" error
credit to pylint docs for example used:
https://pylint.readthedocs.io/en/latest/user_guide/messages/error/no-member.html
'''

class Cat:
    def meow(self):
        print("Meow")

Cat().roar()  
