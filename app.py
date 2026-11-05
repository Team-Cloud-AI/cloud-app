# app.py is the Flet front end for Cloud Financial.
# It uses the Wallet class from safe_to_spend.py, so keep both files in the same folder.
# Run it with:  flet run app.py     (or: python app.py)
#
import flet as ft
from safe_to_spend import Wallet

# colors used throughout the app
SKY = ft.Colors.LIGHT_BLUE_50
CLOUD_BLUE = ft.Colors.LIGHT_BLUE_700
GOOD = ft.Colors.GREEN_700
BAD = ft.Colors.RED_700


def main(page: ft.Page):
    page.title = "Cloud Financial"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = SKY
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH   # cards fill the width
    page.window.width = 440   # phone-sized window on desktop
    page.window.height = 860

    # the app's one wallet; None until the user fills in the setup screen
    state = {"wallet": None, "shown": 0}   # "shown" counts wallet messages already on screen

    # ---------- small helpers ----------
    def money(amount):
        # shows -15.5 as -$15.50 instead of $-15.50
        if amount < 0:
            return f"-${abs(amount):.2f}"
        return f"${amount:.2f}"

    def card(content):
        # a white rounded box used for each section
        return ft.Container(content=content, bgcolor=ft.Colors.WHITE, padding=16,
                            border_radius=16)

    def read_number(field):
        # turns a text field into a number; shows an error on the field if it can't
        try:
            value = float(field.value)
        except (TypeError, ValueError):
            field.error = "Enter a number"
            return None
        if value < 0:
            field.error = "Can't be negative"
            return None
        field.error = None
        return value

    # ---------- setup screen ----------
    def number_field(label, value):
        return ft.TextField(label=label, value=str(value), keyboard_type=ft.KeyboardType.NUMBER,
                            dense=True)

    allowance_in = number_field("Monthly allowance ($)", 1000)
    phone_in = number_field("Phone bill ($)", 50)
    groceries_in = number_field("Groceries ($)", 250)
    eating_out_in = number_field("Eating out ($)", 125)
    emergency_in = number_field("Emergency fund ($)", 200)
    savings_in = number_field("Save first each month ($)", 75)
    goal_in = number_field("Savings goal ($)", 500)
    rate_in = number_field("Save this % of unspent daily money", 50)

    def create_wallet(e):
        fields = [allowance_in, phone_in, groceries_in, eating_out_in, emergency_in,
                  savings_in, goal_in, rate_in]
        values = [read_number(f) for f in fields]
        if None in values:
            page.update()   # shows the error messages on the bad fields
            return
        allowance, phone, groceries, eating_out, emergency, savings, goal, rate = values
        if rate > 100:
            rate_in.error = "Use a number from 0 to 100"
            page.update()
            return
        state["wallet"] = Wallet(allowance=allowance, phone=phone, groceries=groceries,
                                 eatingOut=eating_out, emergency=emergency,
                                 monthly_savings=savings, savings_goal=goal,
                                 save_rate=rate / 100)
        show_dashboard()

    def show_setup():
        page.clean()
        page.add(
            ft.Row([ft.Icon(ft.Icons.CLOUD, color=CLOUD_BLUE, size=36),
                    ft.Text("Cloud Financial", size=26, weight=ft.FontWeight.BOLD)]),
            ft.Text("Let's set up your month. You can change these numbers to match your life."),
            card(ft.Column([
                ft.Text("Money coming in", weight=ft.FontWeight.BOLD),
                allowance_in,
                ft.Text("Monthly costs", weight=ft.FontWeight.BOLD),
                phone_in, groceries_in, eating_out_in, emergency_in,
                ft.Text("Savings", weight=ft.FontWeight.BOLD),
                savings_in, goal_in, rate_in,
            ], spacing=10)),
            ft.FilledButton("Create my wallet", icon=ft.Icons.ACCOUNT_BALANCE_WALLET,
                            on_click=create_wallet),
        )

    # ---------- dashboard screen ----------
    day_text = ft.Text(size=14, color=ft.Colors.GREY_700)
    today_text = ft.Text(size=24, weight=ft.FontWeight.BOLD)
    month_text = ft.Text(size=24, weight=ft.FontWeight.BOLD)
    daily_text = ft.Text(size=12, color=ft.Colors.GREY_700)
    savings_bar = ft.ProgressBar(value=0, bar_height=12, color=GOOD, bgcolor=ft.Colors.GREY_200,
                                 border_radius=6)
    savings_text = ft.Text()
    streak_text = ft.Text()
    nimbus_text = ft.Text("Hi! I'm Nimbus. Log a purchase and I'll check in.", italic=True)
    item_in = ft.TextField(label="What did you buy?", dense=True, expand=True)
    amount_in = ft.TextField(label="Amount ($)", dense=True, width=120,
                             keyboard_type=ft.KeyboardType.NUMBER)
    ask_nimbus_box = ft.Checkbox(label="Ask Nimbus about each purchase (uses API credits)",
                                 value=False)
    activity_list = ft.Column(spacing=4)
    purchases_list = ft.Column(spacing=4)

    def refresh():
        # copies the wallet's numbers onto the screen
        w = state["wallet"]
        day_text.value = f"Day {w.day_counter + 1} of 30"
        today_text.value = money(w.today_left)
        today_text.color = BAD if w.today_left < 0 else GOOD
        month_text.value = money(w.left_over)
        month_text.color = BAD if w.left_over < 0 else GOOD
        daily_text.value = f"Today's budget: {money(w.daily)}"
        if w.savings_goal > 0:
            savings_bar.value = min(w.savings_total / w.savings_goal, 1.0)
        savings_text.value = f"Saved {money(w.savings_total)} of {money(w.savings_goal)}"
        streak_text.value = f"{w.streak}-day under-budget streak"

        # new messages from the wallet (warnings, milestones, streaks) go at the top
        for text in w.messages[state["shown"]:]:
            activity_list.controls.insert(0, ft.Text(f"• {text}", size=13))
        state["shown"] = len(w.messages)

        purchases_list.controls = [
            ft.Row([ft.Text(name, expand=True), ft.Text(money(amount))])
            for name, amount in reversed(w.list_purchases)
        ] or [ft.Text("No purchases yet.", color=ft.Colors.GREY_600)]
        page.update()

    def add_purchase(e):
        w = state["wallet"]
        name = item_in.value.strip() if item_in.value else ""
        item_in.error = None if name else "Enter a name"
        amount = read_number(amount_in)
        if not name or amount is None:
            page.update()
            return
        w.purchase(name, amount)
        item_in.value = ""
        amount_in.value = ""
        refresh()
        if ask_nimbus_box.value:
            nimbus_text.value = "Nimbus is thinking..."
            page.update()
            nimbus_text.value = w.ask_nimbus(name, amount)
            page.update()

    def next_day(e):
        state["wallet"].new_day()
        refresh()

    def start_over(e):
        state["wallet"] = None
        state["shown"] = 0
        activity_list.controls.clear()
        nimbus_text.value = "Hi! I'm Nimbus. Log a purchase and I'll check in."
        show_setup()

    amount_in.on_submit = add_purchase   # pressing Enter in the amount box adds the purchase

    def show_dashboard():
        page.clean()
        page.add(
            ft.Row([ft.Icon(ft.Icons.CLOUD, color=CLOUD_BLUE, size=32),
                    ft.Text("Cloud Financial", size=22, weight=ft.FontWeight.BOLD, expand=True),
                    day_text]),
            # Nimbus speech bubble
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.CLOUD, color=CLOUD_BLUE, size=40),
                                ft.Container(content=nimbus_text, expand=True)]),
                bgcolor=ft.Colors.WHITE, padding=14, border_radius=20,
                border=ft.Border.all(2, CLOUD_BLUE)),
            # what's left today and this month
            ft.Row(vertical_alignment=ft.CrossAxisAlignment.STRETCH, intrinsic_height=True, controls=[
                ft.Container(card(ft.Column([ft.Text("Left today"), today_text, daily_text],
                                            spacing=2)), expand=True),
                ft.Container(card(ft.Column([ft.Text("Left this month"), month_text],
                                            spacing=2)), expand=True),
            ]),
            # savings progress
            card(ft.Column([ft.Text("Savings", weight=ft.FontWeight.BOLD), savings_bar,
                            savings_text,
                            ft.Row([ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color=ft.Colors.ORANGE_700,
                                            size=18), streak_text], spacing=4)], spacing=6)),
            # log a purchase
            card(ft.Column([
                ft.Text("Log a purchase", weight=ft.FontWeight.BOLD),
                ft.Row([item_in, amount_in]),
                ask_nimbus_box,
                ft.FilledButton("Add purchase", icon=ft.Icons.ADD, on_click=add_purchase),
            ], spacing=10)),
            ft.Row([
                ft.Button("End day", icon=ft.Icons.NIGHTLIGHT_ROUND, on_click=next_day),
                ft.TextButton("Start over", on_click=start_over),
            ]),
            card(ft.Column([ft.Text("Activity", weight=ft.FontWeight.BOLD), activity_list])),
            card(ft.Column([ft.Text("Purchases", weight=ft.FontWeight.BOLD), purchases_list])),
        )
        refresh()

    show_setup()


if __name__ == "__main__":
    ft.run(main)
