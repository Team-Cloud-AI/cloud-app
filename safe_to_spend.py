# safe_to_spend.py makes a wallet class which takes out monthly expenses via 
# a constructor whenever a wallet is made and is able to process and saves amount left after purchase via a method.
# Is also able to reset days.
#
#
class Wallet:
    # wallet constructor
    def __init__(self, allowance):
        self.allowance = allowance
        # monthly fixed costs
        phone = 50 
        groceries = 250
        eatingOut = 125
        emergency = 200
        #day setter
        self.day_counter = 0
        self.list_purchases = []
        self.left_over = allowance - phone - groceries - eatingOut - emergency
        # negative budget warning 
        if 0 > self.left_over:
            print("You are going to be negative!!")
        print(round(self.left_over, 2))

        self.daily = self.left_over / 30
        self.today_left = self.daily
        print(round(self.daily, 2))
    # purchase function
    def purchase(self, name, amount):

        self.today_left = self.today_left - amount  #tracks day

        self.left_over = self.left_over - amount #tracks month

        self.list_purchases.append((name, amount))
            

        print(round(self.today_left, 2))
        print(round(self.left_over, 2))
    # day reset function
    def new_day(self): 
        self.day_counter += 1
        self.daily = self.left_over / (30 - self.day_counter)
        self.today_left = self.daily
bmoney = Wallet(1000)
sherlyn = Wallet(500)
bmoney.purchase("lunch", 8)
bmoney.purchase("charger", 20)
bmoney.new_day()
bmoney.purchase("dinner", 6)
print(bmoney.list_purchases)
