import numpy as np
import matplotlib.pyplot as plt
from .errors import NotFittedError


class Strategy:
    """
    Base strategy class with common setup and methods.
    Not intended to be used directly. Instead, use SMA, Momentum or MeanReversion instances.
    """

    def __init__(self, df):
        self.df = df.copy()
        self._fit = False

    def _dropna(self):
        self.df = self.df.dropna()

    def _is_fit(self):
        if not self._fit:
            raise NotFittedError(f'This {self.__class__.__name__} instance is not fitted yet. '
                                 'Call "fit" with appropriate arguments before using this method.')

    def _set_returns(self, metric):
        self.df['returns'] = np.log(self.df[metric] / self.df[metric].shift())
        self._dropna()

    def _set_strategy(self):
        self.df['strategy'] = self.df['returns'] * self.df['position'].shift()
        self._dropna()

    def fit(self, **kwargs):
        for kw, val in kwargs.items():
            setattr(self, kw, val)
        self._set_returns(self.metric)
        self._set_position()
        self._set_strategy()
        self._fit = True

    def plot_strategy(self, plt_kws=None):
        self._is_fit()
        plt_kws = {} if plt_kws is None else plt_kws
        self.df[['returns', 'strategy']].dropna().cumsum().apply(np.exp).plot(**plt_kws)

    def plot_position(self, plt_kws=None):
        self._is_fit()
        plt_kws = {} if plt_kws is None else plt_kws
        self.df.dropna()['position'].plot(**plt_kws)

    def __repr__(self):
        return f'<{self.__class__.__name__}{" fitted" if self._fit else ""}>'


class SMA(Strategy):
    """
    Todo
    """

    def _set_moving_avgs(self, fast, slow, metric):
        if fast >= slow:
            raise ValueError('Fast moving must be less than slow moving average.'
                             f'Got fast: {fast}, slow: {slow}')
        self.df['sma_fast'] = self.df[metric].rolling(fast).mean()
        self.df['sma_slow'] = self.df[metric].rolling(slow).mean()

    def _set_position(self):
        self._set_moving_avgs(self.fast, self.slow, self.metric)
        self.df['position'] = np.where(self.df['sma_fast'] > self.df['sma_slow'], 1, -1)
        self._dropna()

    def fit(self, fast=42, slow=252, metric='adj_close'):
        super().fit(**dict(fast=fast, slow=slow, metric=metric))

    def plot_moving_avgs(self, plt_kws=None):
        self._is_fit()
        plt_kws = {} if plt_kws is None else plt_kws
        self.df[[self.metric, 'sma_fast', 'sma_slow']].dropna().plot(**plt_kws)


class Momentum(Strategy):
    """
    Todo
    """

    def _set_position(self):
        self.df['position'] = np.sign(self.df['returns'].rolling(self.period).mean())
        self._dropna()

    def fit(self, period=3, metric='adj_close'):
        super().fit(**dict(period=period, metric=metric))


class MeanReversion(Strategy):
    """
    Todo
    """

    def _set_moving_avg(self):
        self.df['sma'] = self.df[self.metric].rolling(self.sma).mean()
        self._dropna()

    def _set_distance(self):
        self.df['distance'] = self.df[self.metric] - self.df['sma']
        self._dropna()

    def _set_position(self):
        self._set_moving_avg()
        self._set_distance()
        self.df['position'] = np.where(self.df['distance'] > self.threshold, -1, np.nan)
        self.df['position'] = np.where(self.df['distance'] < -self.threshold, 1, self.df['position'])
        self.df['position'] = np.where(self.df['distance'] * self.df['distance'].shift(1) < 0, 0, self.df['position'])
        self.df['position'] = self.df['position'].ffill().fillna(0)
        self._dropna()

    def fit(self, sma=25, threshold=3.5, metric='adj_close'):
        super().fit(**dict(sma=sma, threshold=threshold, metric=metric))

    def plot_distance(self, plt_kws=None):
        self._is_fit()
        plt_kws = {} if plt_kws is None else plt_kws
        self.df['distance'].dropna().plot(**plt_kws)
        plt.axhline(self.threshold, color='r')
        plt.axhline(-self.threshold, color='r')
        plt.axhline(0, color='k', linestyle='--')
