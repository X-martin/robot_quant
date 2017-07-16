import pandas as pd


class Factor(object):

    def __init__(self, name):
        self.name = name

    def get_factor_values(self, stocks, date):
        df_stocks = pd.DataFrame([stocks], columns=["stock_id"])
        # pass args self.date, self.name, df_factor
        # call Tushare Api
        # df_stocks["factor_value"] = Tushare.get_value(stocks, date)
        #
        return df_stocks

    @staticmethod
    def apply_method(df_factor, method, value):
        if method in ["asc top", "asc bottom", "desc top", "desc bottom"]:
            if value > 0:
                if value < 1:
                    value = int(value * len(df_factor))
                value = min([value, len(df_factor)])
                if method in ["asc top", "desc bottom"]:
                    df_factor = df_factor.sort_values(["factor_value"], ascending=True)
                else:
                    df_factor = df_factor.sort_values(["factor_value"], ascending=False)
                df_factor = df_factor.iloc[:value, :]
        elif method == "is":
            df_factor = df_factor.loc[df_factor["factor_value"] == value]
        elif method == "not":
            df_factor = df_factor.loc[df_factor["factor_value"] != value]
        elif method == "in":
            df_factor = df_factor.loc[df_factor["factor_value"].apply(
                lambda x: x in value)]
        elif method == "not in":
            df_factor = df_factor.loc[df_factor["factor_value"].apply(
                lambda x: x not in value)]
        elif method == "greater":
            df_factor = df_factor.loc[df_factor["factor_value"] > value]
        elif method == "less":
            df_factor = df_factor.loc[df_factor["factor_value"] < value]
        elif method == "between":
            df_factor = df_factor.loc[df_factor["factor_value"] > value[0]]
            df_factor = df_factor.loc[df_factor["factor_value"] < value[1]]
        return df_factor

    def filter(self, stocks, date, method, value):
        df_factor = self.get_factor_values(stocks, date)
        df_factor = self.apply_method(df_factor, method, value)
        return list(df_factor["stock_id"])


class CustomFactor(Factor):
    def __init__(self, name, supfactor_names, supfactor_method, supfactor_value):
        super(CustomFactor, self).__init__(name)
        self.supfactor_names = supfactor_names
        self.supfactor_method = supfactor_method
        self.supfactor_value = supfactor_value
        self.supfactors = []
        for name in supfactor_names:
            factor = Factor(name)
            self.supfactors += [factor]

    def get_supfactor_values(self, stocks, date):
        dfs = []
        for factor in self.supfactors:
            df = factor.get_factor_values(stocks, date)
            dfs += [df]
        return dfs

    def get_factor_values(self, stocks, date):
        df_stocks = pd.DataFrame([stocks], columns=["stock_id"])
        method = self.supfactor_method
        value = self.supfactor_value
        if method == "greater":
            dfs = self.get_supfactor_values(stocks, date)
            factor_values = dfs[0]["factor_value"] > dfs[1]["factor_value"]
        elif method == "less":
            dfs = self.get_supfactor_values(stocks, date)
            factor_values = dfs[0]["factor_value"] < dfs[1]["factor_value"]
        elif method == "lag":
            date = date - value
            dfs = self.get_supfactor_values(stocks, date)
            factor_values = dfs[0]["factor_value"]
        elif method == "avg":
            dfs = self.get_supfactor_values(stocks, date)
            factor_values = dfs[0]["factor_value"]
            for i in range(1, len(dfs)):
                factor_values += dfs[i]["factor_value"]/float(len(dfs))

        df_stocks.join(factor_values)
        return df_stocks
