class Category:

    # Define __init__ method that take the category name as an argument
    # also initiates 2 things: a list to store transactions and an int = 0 to track funds.
    def __init__(self, name):
        self.name = name # instance variable, category name is stored inside the object
        self.ledger = [] # instance variable, a ledger list to store transactions
        self.balance = 0 # instance variable (to track available funds later)

    # Define a `deposit` method that accepts an amount and description.
    def deposit(self, amount, description=""): # Desctiption is optional, thus pass an empty str
        self.ledger.append({"amount": amount, "description": description}) # stores and adds a transaction as one disctionary
        self.balance += amount # modifies the remaining amount

    # Define a withdraw method -> similar to deposit, but with the opposite sign.
    # Also add a condition: I cannot withdraw more money than I have. In this case return False, otherwise True.
    def withdraw(self, amount, description=""):
        if amount > self.balance:
            return False
        else:
            self.ledger.append({"amount": -amount, "description": description})
            self.balance -= amount
            return True

    # Define a `get_balance` method that returns the current balance of the budget category (simply return self.balance)
    def get_balance(self):
        return self.balance

    # Define a `transfer` method that accepts an amount and another budget category as arguments.
    def transfer(self, amount, name):
        if self.balance < amount: # if the amount is bigger than the balance, return False (no transaction!)
            return False
        else: # else return True
            self.withdraw(amount, f"Transfer to {name.name}") # call withdraw with self
            name.deposit(amount, f"Transfer from {self.name}") # call withraw with the other category's name
            return True

    # Define a `check_funds` method that accepts an amount as an argument. Should return False if entered amount > outstanding balance, else True
    def check_funds(self, amount):
        if amount > self.balance:
            return False
        else:
            return True

    # Define a method to customise the printed result with __str__ method
    def __str__(self):
        # create a title for our printed message
        title_message = self.name.center(30,'*')
        transaction_messages = [] # a list where all the transaction messages will be stored

        # now I need to get the description and amounts
        for item in range(len(self.ledger)):
            message_desc = self.ledger[item]['description'][:min(23, len(self.ledger[item]['description']))].ljust(23)
            # min(either 23 characters or the length of the description)
            # .ljust(23) align left within 23 spaces
            message_amount = f"{self.ledger[item]['amount']:.2f}".rjust(7)
            # amount is an intiger. Format it with f-string, this will turn it into a string. .rjust -> align right within 7 spaces
            # join two messages into a transaction message
            transaction_messages.append(f'{message_desc}{message_amount}')
        all_transactions = '\n'.join(transaction_messages) # transaction_messages list is transaformed into one string, where messages are separated by a newline
        return f'{title_message}\n{all_transactions}\nTotal: {self.balance:.2f}'
        # f'intiger:.2f' returns two decimal places

def create_spend_chart(categories):
    # create a title message
    chart_title = f'Percentage spent by category\n'
    # calculate total withdrawals by going through each category
    total_withdrawals = 0
    for cat in categories:
        # access the dictionary of each category
        for cash_out in cat.ledger:
            # get all the negative amounts in the dictionary
            if cash_out['amount'] < 0:
                # sum them up
                total_withdrawals += abs(cash_out['amount']) # this one will generate the total amount
    
    # now do the same to calculate the percentage
    category_withdrawals_dict = {}
    category_percentage_dict = {}
    for cat in categories:
        category_withdrawals = 0 # here will be stored the total withdrawal per category
        for cash_out in cat.ledger:
            if cash_out['amount'] < 0:
                category_withdrawals += abs(cash_out['amount'])
        # store total withdrawals per category in a dictionary (with a key)
        category_withdrawals_dict[cat.name] = category_withdrawals
        # Calculate rounded percentage (do to nearest 10)
        category_percentage_dict[cat.name] = (category_withdrawals_dict[cat.name] / total_withdrawals) * 100 // 10 * 10
    
    # create the left-side percentage message
    o_message = ''
    final_message = ''
    for percent in range(100,-1,-10):
        o_message = (str(percent)).rjust(3)+"| "
        for cat in categories:
            if category_percentage_dict[cat.name] >= percent:
                o_message += "o  "
            else:
                o_message += "   "
        final_message += o_message + "\n"
    
    # one space before a category, and two spaces after.
    # 4 spaces before + (1 + 3n)
    dashes = " " * 4 + "-" * (1 + 3 * len(categories)) + "\n"
    
    # find the longest category name and its length
    # this length will help to print out all letter vertically
    longest_cat_name = 0
    for cat in categories:
        if len(cat.name) > longest_cat_name:
            longest_cat_name = len(cat.name)
    
    category_print_list = [] # here will be stored the list with category names prints
    for letter_position in range(0, longest_cat_name):
        # 5 first spaces empty then a letter and 2 spaces after that
        category_print = " " * 5
        for cat in categories:
            if letter_position < len(cat.name): 
                category_print += cat.name[letter_position] + " " * 2 # print if there is a letter and add 2 spaces afterwards
            else:
                # print 3 spaces (one for the letter, 2 after that)
                category_print += " " * 3
        category_print_list.append(category_print)
    
    # now join all strings within the list into one string.
    category_print_vertical = "\n".join(category_print_list)

    # return the final result for the print
    return f'{chart_title}{final_message}{dashes}{category_print_vertical}'
