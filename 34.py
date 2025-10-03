class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner         
        self.balance = float(balance)  

    def deposit(self, amount):
        if amount <= 0:
            print("Сумма пополнения должна быть положительной.")
        else:
            self.balance += amount
            print(f"Пополнение: {amount}. Новый баланс: {self.balance}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Сумма снятия должна быть положительной.")
        elif amount > self.balance:
            print("Ошибка: недостаточно средств на счёте.")
        else:
            self.balance -= amount
            print(f"Снятие: {amount}. Остаток: {self.balance}")

    def __str__(self):
        return f"Счёт владельца {self.owner}. Баланс: {self.balance}"


acc = Account("Алихан", 100)   
print(acc)

acc.deposit(50)   
acc.withdraw(30)  
acc.withdraw(200) 
print(acc)
