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
        self.left_over = allowance - phone - groceries - eatingOut - emergency
        print(self.left_over)

        self.daily = self.left_over / 30
        self.today_left = self.daily
        print(self.daily)
    # purchase function
    def purchase(self, name, amount):

        self.today_left = self.today_left - amount  #tracks day

        self.left_over = self.left_over - amount #tracks month

        print(self.today_left)
        print(self.left_over)
    # day reset function
    def new_day(self): 
        self.today_left = self.daily
bmoney = Wallet(1000)
bmoney.purchase("lunch", 8)
bmoney.purchase("charger", 20)
bmoney.new_day()
bmoney.purchase("dinner", 6)
