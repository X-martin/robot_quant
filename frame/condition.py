# -------------------------------------


class Condition(object):
    def __init__(self, factor, method, value):
        self.factor = factor
        self.method = method
        self.value = value
        self.stocks = []

    def filter(self, stocks, date):
        self.stocks = self.factor.filter(stocks, date, method, value)
        return set(self.stocks)


class ConditionTree(object):
    def __init__(self, node, left=None, right=None):
        self.node = node
        self.left = left
        self.right = right

    def search(self, stocks, date):
        if self.node == "union":
            return self.left.search(stocks, date).union(self.right.search(stocks, date))
        elif self.node == "intersection":
            return self.left.search(stocks, date).intersection(self.right.search(stocks, date))
        elif self.node == "difference":
            return self.left.search(stocks, date).difference(self.right.search(stocks, date))
        elif self.node == "symmetric_difference":
            return self.left.search(stocks, date).symmetric_difference(self.right.search(stocks, date))
        else:
            return self.node.filter(stocks, date)
