import pandas as pd


class Factor(object):

    def __init__(self, name, method):
        self.name = name
        self.method = method
        self.date = None
        self.stocks = pd.DataFrame(columns=["stock_id", "value"])

    def get_values(self):
        # pass args self.date, self.name, self.stocks
        # call Tushare Api
        # rewrite self.values
        pass

    def apply_method(self):
        method = self.method[0]
        quant = self.method[1]
        if method == "asc top":
            pass
        elif method == "asc bottom":
            pass
        elif method == "desc top":
            pass
        elif method == "desc bottom":
            pass
        elif method == "is":
            pass
        elif method == "not":
            pass
        elif method == "in":
            pass
        elif method == "not in":
            pass
        elif method == "greater":
            pass
        elif method == "less":
            pass
        elif method == "between":
            pass

    def filter(self, stocks, date):
        self.stocks["stock_id"] = stocks
        self.date = date
        self.get_values()
        self.apply_method()
        return list(self.stocks["stock_id"])
