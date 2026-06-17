class Category:
    """
    A class to represent a spending category (e.g., Food, Clothing).
    Each category keeps a ledger of transactions.
    """

    def __init__(self, name):
        """
        Initialize a new Category instance.
        :param name: The name of the category (string)
        """
        self.name = name               # Store the category name
        self.ledger = []               # List of dictionaries: each is a transaction

    def deposit(self, amount, description=""):
        """
        Add a positive amount to the ledger.
        :param amount: The amount to deposit (float)
        :param description: Optional text describing the deposit (default empty)
        """
        # Append a transaction dictionary with the amount and description
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        """
        Remove a positive amount from the ledger (store as negative).
        Only succeeds if funds are sufficient.
        :param amount: The amount to withdraw (float)
        :param description: Optional text describing the withdrawal (default empty)
        :return: True if successful, False if insufficient funds
        """
        # check_funds() tells us if we have enough balance
        if self.check_funds(amount):
            # Store the amount as a negative number to represent a withdrawal
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        """
        Calculate the current balance of this category.
        :return: Sum of all amounts in the ledger (float)
        """
        # Sum the 'amount' values from every transaction in the ledger
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, category):
        """
        Transfer money from this category to another category.
        :param amount: The amount to transfer (float)
        :param category: The destination Category instance
        :return: True if successful, False if insufficient funds
        """
        # Only proceed if we have enough balance
        if self.check_funds(amount):
            # Withdraw from this category with a special description
            self.withdraw(amount, f"Transfer to {category.name}")
            # Deposit into the destination category with a matching description
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        """
        Check if the given amount is available in the current balance.
        This method is reused by both withdraw() and transfer().
        :param amount: The amount to check (float)
        :return: True if amount <= balance, False otherwise
        """
        return amount <= self.get_balance()

    def __str__(self):
        """
        Create a human-readable representation of the category,
        following the exact formatting required by the lab.
        :return: A formatted multi-line string
        """
        # --- 1. Title line: 30 characters total with the category name centered
        # Calculate padding on left and right to center the name
        left_padding = (30 - len(self.name)) // 2
        right_padding = 30 - len(self.name) - left_padding
        # Build the title: asterisks, name, asterisks
        title = "*" * left_padding + self.name + "*" * right_padding

        # Start the output with the title
        lines = [title]

        # --- 2. Ledger entries: each on its own line
        for item in self.ledger:
            # Truncate description to at most 23 characters
            description = item["description"][:23]
            amount = item["amount"]
            # Format: description left-aligned in 23 spaces, amount right-aligned
            # in 7 spaces with 2 decimal places (e.g. " 1000.00")
            lines.append(f"{description:<23}{amount:>7.2f}")

        # --- 3. Final line showing the total balance
        lines.append(f"Total: {self.get_balance():.2f}")

        # Join all lines with newline characters and return
        return "\n".join(lines)


def create_spend_chart(categories):
    """
    Create a bar chart (as a string) showing the percentage of spending
    for each category, based only on withdrawals (not deposits).
    :param categories: A list of Category instances
    :return: A multi-line string representing the chart
    """
    # --- Step 1: Calculate total withdrawals (spent) for each category
    withdrawals = []   # List of total spent amounts, one per category
    for cat in categories:
        spent = 0
        for item in cat.ledger:
            # Negative amount means it's a withdrawal (money spent)
            if item["amount"] < 0:
                spent += -item["amount"]   # convert negative to positive
        withdrawals.append(spent)

    # Total spent across all categories
    total_spent = sum(withdrawals)

    # --- Step 2: Convert each spent amount to a percentage of total,
    # rounded down to the nearest 10 (e.g., 42% --> 40%)
    percentages = []
    for spent in withdrawals:
        if total_spent == 0:
            # Avoid division by zero: if nothing was spent, percentage is 0
            p = 0
        else:
            p = int((spent / total_spent) * 100)   # integer percentage
            p = (p // 10) * 10                     # round down to nearest 10
        percentages.append(p)

    # --- Step 3: Build the chart string line by line

    # Title
    chart = "Percentage spent by category\n"

    # Y-axis labels from 100 down to 0, step 10
    for y in range(100, -10, -10):
        # Right-align the number in 3 spaces, then add "| "
        chart += str(y).rjust(3) + "| "

        # For each category's percentage, decide if a bar should be drawn
        # at this vertical level. We use 'o' for the bar (the official spec).
        # If your tests expect '#', you can replace 'o' with '#' here.
        for p in percentages:
            if p >= y:
                chart += "o  "   # bar + two spaces
            else:
                chart += "   "   # three spaces (empty)
        # End of this y-level line
        chart += "\n"

    # --- Step 4: Horizontal line below the bars
    # 4 spaces ("    ") then a dash for each column.
    # Each column is 3 characters wide: 1 char (bar or space) + 2 spaces.
    # So total dashes = (number of categories * 3) + 1
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # --- Step 5: Write category names vertically below the bars
    # Find the longest category name to know how many vertical lines we need
    max_name_length = max(len(cat.name) for cat in categories)

    # For each character position from 0 to max_length-1
    for i in range(max_name_length):
        # Start with 5 spaces before the first letter (to align under the dashes)
        chart += "     "

        # For each category, print the i-th character if it exists,
        # otherwise print three spaces (to keep alignment)
        for cat in categories:
            if i < len(cat.name):
                chart += cat.name[i] + "  "   # letter + two spaces
            else:
                chart += "   "                # three spaces as placeholder

        # Move to the next line (except after the last line, we'll strip it later)
        chart += "\n"

    # Remove the very last newline (to match expected output exactly)
    return chart.rstrip("\n")

#######################

food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
clothing = Category("Clothing")
food.transfer(50, clothing)

print(food)