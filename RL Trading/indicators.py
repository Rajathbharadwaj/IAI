import pandas_ta as ta
import pandas as pd


class Indicators:
    """
    Calculates the custom indicators needed for trading
    SuperTrend -> {15 0.8, 10 0.6}
    Moving Averages -> {DEMA : {}}
    """

    def __init__(self, dataframe, ):
        self.dataframe = dataframe
        # self.dataframe.set_index('date', inplace=True)
        self.totalIndicators = pd.DataFrame()

    def calSuperTrend(self, len1=7, mul1=1, ):
        dataframe = self.dataframe
        # superTrend15_35 = ta.supertrend(dataframe['high'], dataframe['low'], dataframe['close'],
        #                                 length=len1, multiplier=mul1)
        # superTrend4_1 = ta.supertrend(dataframe['high'], dataframe['low'], dataframe['close'],
        #                               length=len2, multiplier=mul2)
        # superTrend10_12 = ta.supertrend(dataframe['high'], dataframe['low'], dataframe['close'],
        #                                 length=len3, multiplier=mul3)
        # superTrend15_14 = ta.supertrend(dataframe['high'], dataframe['low'], dataframe['close'],
        #                                 length=len4, multiplier=mul4)
        superTrend4_06 = dataframe.ta.supertrend(len1, mul1)
        # superTrend4_2 = dataframe.ta.supertrend(len5, mul5)
        self.totalIndicators = pd.concat([superTrend4_06, ], axis=1)

    def calPSAR(self,):
        dataframe = self.dataframe
        psar_val = dataframe.ta.psar(af=0.02, max_af=0.2)
        self.totalIndicators = pd.concat([self.totalIndicators, psar_val], axis=1)

    def movingAverages(self, ):
        dataframe = self.dataframe
        ma5 = dataframe.ta.sma(5)
        wma10 = dataframe.ta.wma(10)
        sma14 = dataframe.ta.sma(14)
        wma28 = dataframe.ta.wma(28)
        sma44 = dataframe.ta.sma(44)
        self.totalIndicators = pd.concat([self.totalIndicators, ma5, wma10, sma14, wma28, sma44], axis=1)

    def rsiC(self, ):
        dataframe = self.dataframe
        rsi_value = dataframe.ta.rsi(14)
        self.totalIndicators = pd.concat([self.totalIndicators, rsi_value], axis=1)

    def vwap(self, ):
        try:
            dataframe = self.dataframe
            vwap = dataframe.set_index('DateTime').ta.vwap()
            print(f"this is vwap -> {vwap}")
            self.totalIndicators['VWAP_D'] = pd.Series(vwap.to_list())
            self.totalIndicators = pd.concat([self.totalIndicators], axis=1)
        except Exception as e:
            print(e)
            pass

    def returnIndicators(self, ):

        self.calSuperTrend()
        self.movingAverages()
        self.calPSAR()
        # self.vwap()
        return pd.concat([self.dataframe, self.totalIndicators], axis=1)

