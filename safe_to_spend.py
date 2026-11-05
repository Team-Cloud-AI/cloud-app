# safe_to_spend.py makes a wallet class which takes out monthly expenses via 
# a constructor whenever a wallet is made and is able to process and saves amount left after purchase via a method.
# Is also able to reset days.
#
#
import anthropic
client = anthropic.Anthropic()
NIMBUS_PROMPT = """You are Nimbus, the cloud mascot for Cloud Financial, a budgeting app.
You talk to someone new to budgeting, usually a neurodivergent young adult who just moved out or started college.
You react to their purchases, what they have left today and this month, and any spending patterns you notice.
Be strict about money. Only joke when there's a clear opening, keep humor obvious, never sarcastic, and never be mean.
Never use more than 18 words."""
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
    
        #monthly and daily changes to total
        print(f"Left Today: ${self.today_left:.2f}")
        print(f"Left this month: ${self.left_over:.2f}")
    def ask_nimbus(self, name, amount):
        message = f"this is the name of the purchase the user made {name} and this is the amount that it cost {amount}"
                
    # day reset function
    def new_day(self): 
        self.day_counter += 1
        if self.day_counter == 30:
            self.left_over = self.allowance - self.phone - self.groceries - self.eatingOut - self.emergency
            self.day_counter = 0
        self.daily = self.left_over / (30 - self.day_counter)
        self.today_left = self.daily
    #Summary of Purchases 
    def summary_purchases(self):
        print("=====SUMMARY=====")
        for name, amount in self.list_purchases:
            print(f"{name}: ${amount:.2f}")
#calls wallet
bmoney = Wallet(1000)
#sample purchases
bmoney.purchase("lunch", 8)
bmoney.purchase("charger", 20)
bmoney.new_day()
bmoney.purchase("dinner", 6)
bmoney.summary_purchases()
#test: 31 days to check month reset
for i in range(31):
    bmoney.new_day()
    print(round(bmoney.daily, 2))