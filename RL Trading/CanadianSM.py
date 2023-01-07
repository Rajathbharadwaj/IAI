import numpy as np
from gym_anytrading.envs.trading_env import TradingEnv, Actions, Positions


class CanadianSM(TradingEnv):

    def __init__(self, df, window_size, frame_bound):
        self.frame_bound = frame_bound,
        super().__init__(df, window_size)

        self.trade_fee_bid_percent = 0.01
        self.trade_fee_ask_percent = 0.05
