import pandas as pd


class Factor(object):

    def __init__(self, name):
        self.name = name
        self.method = None
        self.value = None
        self.date = None
        self.stocks = pd.DataFrame(columns=["stock_id", "factor_value"])

    def get_factor_values(self):
        # pass args self.date, self.name, self.stocks
        # call Tushare Api
        # rewrite self.values
        pass

    def apply_method(self):
        if method in ["asc top", "asc bottom", "desc top", "desc bottom"]:
            if self.value > 0:
                if self.value < 1:
                    self.value = int(self.value * len(self.stocks))
                self.value = min([self.value, len(self.stocks)])
                if method in ["asc top", "desc bottom"]:
                    self.stocks = self.stocks.sort_values(["factor_value"], ascending=True)
                else:
                    self.stocks = self.stocks.sort_values(["factor_value"], ascending=False)
                self.stocks = self.stocks.iloc[:self.value, :]
        elif method == "is":
            self.stocks = self.stocks.loc[self.stocks["factor_value"] == self.value]
        elif method == "not":
            self.stocks = self.stocks.loc[self.stocks["factor_value"] != self.value]
        elif method == "in":
            self.stocks = self.stocks.loc[self.stocks["factor_value"].apply(
                lambda x: x in self.value)]
        elif method == "not in":
            self.stocks = self.stocks.loc[self.stocks["factor_value"].apply(
                lambda x: x not in self.value)]
        elif method == "greater":
            self.stocks = self.stocks.loc[self.stocks["factor_value"] > self.value]
        elif method == "less":
            self.stocks = self.stocks.loc[self.stocks["factor_value"] < self.value]
        elif method == "between":
            self.stocks = self.stocks.loc[self.stocks["factor_value"] > self.value[0]]
            self.stocks = self.stocks.loc[self.stocks["factor_value"] < self.value[1]]

    def filter(self, stocks, date, method, value):
        self.stocks["stock_id"] = stocks
        self.date = date
        self.method = method
        self.value = value
        self.get_factor_values()
        self.apply_method()
        return list(self.stocks["stock_id"])
