import math

class Category:
    
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.ledger = []

    # This method append an object to the ledger list with negative amount
    def deposit(self, amount, description=''):
        self.ledger.append({"amount": amount, "description": description})
        self.balance += amount

    # This method append an object to the ledger list with negative amount
    # if the amount is smaller or equal to the balance
    # It returns True if the withdraw is made, returns False otherwise
    def withdraw(self, amount, description=''):
        if not self.check_funds(amount):
            return False
        self.ledger.append({"amount": 0 - amount, "description": description})
        self.balance -= amount
        return True

    # This method returns the current balance
    def get_balance(self):
        return self.balance
    
    # This method withdraws amount from one category and deposit it to the target Category
    # It returns True if the transfer is made, returns False otherwise
    def transfer(self, amount, destination_category):
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, "Transfer to " + destination_category.name)
        destination_category.deposit(amount, "Transfer from " + self.name)
        return True

    # This method returns True if a category balance is equal or more than a given amount
    def check_funds(self, amount):
        if amount > self.balance:
            return False
        else:
            return True

    def __str__(self):
        output_array = []
        output_array.append(self.name.center(30, '*'))
        for item in self.ledger:
            item_string = item['description'][:23].ljust(23) + '{:>7.2f}'.format(item['amount'])
            output_array.append(item_string)
        output_array.append('Total: {}'.format(self.balance))

        output = '\n'.join(output_array)  
        return output


def create_spend_chart(categories):
    
    # caculate the spending by each ategory
    category_spending = []
    for category in categories:
        spending = 0
        for item in category.ledger:
            if item['amount'] < 0:
                spending += item['amount'] * -1
        category_spending.append(spending)

    # set bar length by spending percentage
    percentage_bar = [math.floor((x /sum(category_spending)) * 10) + 1 for x in category_spending ]

    # set top half of the graph
    header = 'Percentage spent by category\n'
    y_axis = ['{:>3}|'.format(x) for x in range(100, -1, -10)]

    # graph area
    graph = []
    for percentage in percentage_bar:
        bar = 'o' * percentage
        bar_array = [ char for char in bar.rjust(11)]
        graph.append(bar_array)

    arranged_graph = []
    for index in range(len(y_axis)):
        line = []
        for column in range(len(graph)):
            line.append(graph[column][index] + '  ')
        arranged_graph.append(''.join(line))
    
    # combine y-axis and graph
    mid_section = []
    for index in range(len(y_axis)):
        mid_section.append(y_axis[index] + ' ' + arranged_graph[index])
    
    break_line = '    ' + '-' * ( 1 + len(categories) * 3) + '\n'
    graph_str = '\n'.join(mid_section) + '\n' + break_line

    # set bottom half of the graph
    name_max_len = None
    for category in categories:
        if name_max_len is None or len(category.name) > name_max_len:
            name_max_len = len(category.name)
    
    x_axis_array = []
    for category in categories:
        name_array = [ char for char in category.name.ljust(name_max_len)]
        x_axis_array.append(name_array)

    arragned_x_axis = []
    for index in range(name_max_len):
        line = []
        for column in range(len(x_axis_array)):
            line.append(x_axis_array[column][index] + '  ')
        arragned_x_axis.append(' ' * 5 + ''.join(line))

    x_axis_str = '\n'.join(arragned_x_axis)

    # combine all parts of the graph
    output = header + graph_str + x_axis_str

    return output