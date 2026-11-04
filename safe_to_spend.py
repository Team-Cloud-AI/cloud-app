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
        self.phone = 50 
        self.groceries = 250
        self.eatingOut = 125
        self.emergency = 200
        #day setter
        self.day_counter = 0
        #list of purchases
        self.list_purchases = []
        self.left_over = allowance - self.phone - self.groceries - self.eatingOut - self.emergency
        # negative budget warning 
        if 0 > self.left_over:
            print("You are going to be negative!!")
        print(f"Monthly budget: ${self.left_over:.2f}")

        self.daily = self.left_over / 30
        self.today_left = self.daily
        print(f"Daily Budget: ${self.daily:.2f}")
    # purchase function
    def purchase(self, name, amount):

        self.today_left = self.today_left - amount  #tracks day

        self.left_over = self.left_over - amount #tracks month
        # fills the list made in __init__ with purchases
        self.list_purchases.append((name, amount))
        if 0 > self.today_left:
            print("You are negative for the day!!")
            

        print(f"Left Today: ${self.today_left:.2f}")
        print(f"Left this month: ${self.left_over:.2f}")
    # day reset function
    def new_day(self): 
        self.day_counter += 1
        if self.day_counter == 30:
            self.left_over = self.allowance - self.phone - self.groceries - self.eatingOut - self.emergency
            self.day_counter = 0
        self.daily = self.left_over / (30 - self.day_counter)
        self.today_left = self.daily
bmoney = Wallet(1000)
bmoney.purchase("lunch", 8)
bmoney.purchase("charger", 20)
bmoney.new_day()
bmoney.purchase("dinner", 6)
print(bmoney.list_purchases)
for i in range(31):
    bmoney.new_day()
    print(round(bmoney.daily, 2))
