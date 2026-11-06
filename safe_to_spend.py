# safe_to_spend.py creates a Wallet that subtracts monthly expenses and savings when it is made,
# tracks purchases against daily and monthly budgets, and resets each day and month.
# Savings incentives: pay yourself first, unspent daily money moves to savings,
# under-budget streaks, and milestone messages toward a savings goal.
#
import anthropic
#connection to anthropic API, send messages to claude
client = anthropic.Anthropic()
#claude prompt for mascot
AI_PROMPT = """You are AI, a friendly, playful cloud mascot for Cloud Financial, a budgeting app.
Your voice is upbeat and a little silly. Include one cloud pun in every reply, such as "let's clear the sky," "that's a storm cloud on your wallet," or "you're floating on fumes."
The user is new to budgeting, often a neurodivergent young adult. Make them feel cheered on, never judged.
Every message names the item they just bought, its price, and what is left today and this month.
Reply in two to three short sentences, under 45 words. Name the item, use one real number, and end with one concrete next step.
Never shame them and never be sarcastic or mean."""
class Wallet:
    # wallet constructor; creates the wallet
    def __init__(self, allowance, phone, groceries, eatingOut, emergency,
                 monthly_savings, savings_goal, save_rate):
        #total amount of money for month
        self.allowance = allowance
        # monthly fixed costs, passed in when the wallet is created
        self.phone = phone #phone bill allocation
        self.groceries = groceries #cost of groceries
        self.eatingOut = eatingOut #cost of eating out
        self.emergency = emergency #cost of emergencies
        # savings settings
        self.monthly_savings = monthly_savings #saved first each month (pay yourself first)
        self.savings_goal = savings_goal #total amount the user is saving toward
        self.save_rate = save_rate #share of unspent daily money moved to savings, 0.5 means half
        # savings tracking
        self.savings_total = monthly_savings #first month's savings go in right away
        self.streak = 0 #days in a row the user stayed under budget
        self.milestones = [25, 50, 75, 100] #percent of the goal that earns a message
        self.milestones_reached = [] #milestones already celebrated, so each prints once
        #day setter; day of the month ; increments with each new day
        self.day_counter = 0
        #list of purchases
        self.list_purchases = []
        #messages for the user; a front end (like the Flet app) can read and show these
        self.messages = []
        self.left_over = self.monthly_spending_money() #whats left after monthly costs and savings
        # negative budget warning
        if self.left_over < 0:
            self.say("You are going to be negative!!")
        print(f"Monthly budget: ${self.left_over:.2f}")

        self.daily = self.left_over / 30            #budget for today
        self.today_left = self.daily                   #amount available for each day and decrements with each purchase
        print(f"Daily Budget: ${self.daily:.2f}")
        print(f"Savings: ${self.savings_total:.2f} of ${self.savings_goal:.2f} goal")
        self.check_milestones()
    # prints a message and saves it in self.messages so a front end can show it too
    def say(self, text):
        print(text)
        self.messages.append(text)
    # spending money left after the monthly costs and savings; used by __init__ and new_day
    def monthly_spending_money(self):
        return (self.allowance - self.phone - self.groceries - self.eatingOut
                - self.emergency - self.monthly_savings)
    # purchase function
    def purchase(self, name, amount):

        self.today_left = self.today_left - amount  #tracks day

        self.left_over = self.left_over - amount #tracks month
        # fills the list made in __init__ with purchases
        self.list_purchases.append((name, amount))
        if self.today_left < 0:
            self.say("You are negative for the day!!")

        #monthly and daily changes to total
        print(f"Left Today: ${self.today_left:.2f}")
        print(f"Left this month: ${self.left_over:.2f}")
    def ask_ai(self, name, amount):
        message = (f"this is the name of the purchase the user made {name} and this is the amount that it cost {amount} "
                   f"and there is {self.left_over:.2f} left for the month and {self.today_left:.2f} left for the day. "
                   f"They have saved {self.savings_total:.2f} of their {self.savings_goal:.2f} goal "
                   f"and have stayed under budget {self.streak} days in a row.")
        if client.api_key is None:
            return "AI is offline. Set ANTHROPIC_API_KEY to hear from AI."
        try:
            response = client.messages.create(
                model="claude-haiku-5-5",
                max_tokens=1000,
                thinking={"type": "disabled"},
                system=AI_PROMPT,
                messages=[{"role": "user", "content": message}],
            )
        except anthropic.APIError as error:
            return f"AI couldn't connect right now ({error.__class__.__name__})."
        reply = ""
        for block in response.content:
            if block.type == "text":
                reply += block.text
        return reply
    # moves part of today's unspent money into savings and updates the streak
    def end_of_day_savings(self):
        if self.today_left >= 0:
            saved = self.today_left * self.save_rate
            self.savings_total += saved
            self.left_over -= saved #saved money leaves the spending budget
            self.streak += 1
            self.say(f"Under budget! ${saved:.2f} moved to savings. Streak: {self.streak} day(s)")
            if self.streak % 7 == 0:
                self.say(f"{self.streak} days in a row under budget. Great habit!")
        else:
            if self.streak > 0:
                self.say(f"Over budget today, so your {self.streak}-day streak resets. Tomorrow is a fresh start.")
            self.streak = 0
        self.check_milestones()
    # prints a message the first time savings pass each milestone
    def check_milestones(self):
        if self.savings_goal <= 0:
            return
        for percent in self.milestones:
            if percent not in self.milestones_reached and self.savings_total >= self.savings_goal * percent / 100:
                self.milestones_reached.append(percent)
                self.say(f"Milestone! You reached {percent}% of your ${self.savings_goal:.2f} savings goal!")
    # day reset function
    def new_day(self):
        self.end_of_day_savings() #close out today before starting a new one
        self.day_counter += 1
        if self.day_counter == 30:
            self.left_over = self.monthly_spending_money()
            self.savings_total += self.monthly_savings #pay yourself first for the new month
            self.day_counter = 0
            self.say(f"New month! ${self.monthly_savings:.2f} added to savings.")
            self.check_milestones()
        self.daily = self.left_over / (30 - self.day_counter)
        self.today_left = self.daily
    #Summary of Purchases
    def summary_purchases(self):
        print("=====SUMMARY=====")
        for name, amount in self.list_purchases:
            print(f"{name}: ${amount:.2f}")
    #Summary of Savings
    def summary_savings(self):
        print("=====SAVINGS=====")
        print(f"Saved: ${self.savings_total:.2f} of ${self.savings_goal:.2f}")
        print(f"Under-budget streak: {self.streak} day(s)")
# test code only runs when this file is run directly, not when the Flet app imports it
if __name__ == "__main__":
    #calls wallet; keyword arguments make it clear which number is which
    bmoney = Wallet(allowance=1000, phone=35, groceries=120, eatingOut=60, emergency=180,
                    monthly_savings=75, savings_goal=500, save_rate=0.5)
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
    bmoney.summary_savings()