# ----------------------------------
# import condition as cd


class Portfolio(object):

    def __init__(self, universe, t_start, t_end, dt, condition_buy, condition_sell):
        self.universe = universe
        self.stocks_u = []
        self.stocks_sell = []
        self.stocks_buy = []
        self.t_start = t_start
        self.t_end = t_end
        self.t_current = t_start
        self.dt = dt
        self.t_list_trade = []
        self.t_list_base = []
        self.condition_sell = condition_sell
        self.condition_buy = condition_buy
        self.position = pd.DataFrame(columns=['date', 'stock_id', 'volume', 'price'])

    def get_t_list(self):
        self.t_list_trade = []
        self.t_list_base = []

    def trigger(self):
        self.stocks_sell = self.condition_sell.search(self.stocks_u, self.t_current)
        self.stocks_buy = self.condition_buy.search(self.stocks_u, self.t_current)

    def trade(self):
        for stock in self.stocks_buy:
            if stock in self.stocks_sell:
                self.stocks_buy.remove(stock)
        stocks_current = list(self.position['stock_id'])
        if stocks_current != self.stocks_buy:
            pass

    def update_position(self):
        pass

    def backtesting(self):
        for self.t_current in self.t_list_base:
            self.update_position()
            if self.t_current in self.t_list_trade:
                self.trigger()
                self.trade()
            self.push2db()

    def push2db(self):
        pass
