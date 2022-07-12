import numpy as np
import matplotlib.pyplot as plt
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter
from bokeh.embed import components
from .errors import NotFittedError


class Strategy:
    """
    Base strategy class with common setup and methods.
    Not intended to be used directly. Instead, use SMA, Momentum or MeanReversion instances.
    """

    def __init__(self, df, short_pos=0):
        if 'date' not in df:
            raise KeyError('Expected a datetime column "date" in the input DataFrame.')
        self.df = df.copy().set_index('date')
        self._fit = False
        self.short_pos = short_pos

    def _dropna(self):
        self.df = self.df.dropna()

    def _check_fitted(self):
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
        self._check_fitted()
        plt_kws = {} if plt_kws is None else plt_kws
        self.df[['returns', 'strategy']].dropna().cumsum().apply(np.exp).plot(**plt_kws)

    def plot_position(self, plt_kws=None):
        self._check_fitted()
        plt_kws = {} if plt_kws is None else plt_kws
        self.df.dropna()['position'].plot(**plt_kws)

    def _get_plot_title(self, stock):
        if stock:
            metric = self.metric.replace('_', ' ').title()
            return (f'{stock.name} ({stock.symbol}) {metric} Price | {self.fast} and {self.slow} Day Moving Averages | '
                    f'{self.df.index.min().strftime("%b-%Y")} - {self.df.index.max().strftime("%b-%Y")}')

    def get_bokeh_components(self, stock=None):
        self._check_fitted()
        title = self._get_plot_title(stock)
        p = figure(
            title=title,
            x_axis_label="Date",
            y_axis_label="Price",
            sizing_mode='stretch_width',
            height=350
        )

        source = ColumnDataSource(self.df.dropna())

        p.line(x='date', y='adj_close', source=source, legend_label="Price")
        p.line(x='date', y='sma_fast', source=source, color='green', legend_label=f'MA-{self.fast}')
        p.line(x='date', y='sma_slow', source=source, color='red', legend_label=f'MA-{self.slow}')

        p.legend.location = 'top_left'

        # Format x-axis
        p.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
        p.xaxis[0].formatter = DatetimeTickFormatter(months="%Y")

        return components(p)

    def __repr__(self):
        return f'<{self.__class__.__name__}{" fitted" if self._fit else ""}>'

    def get_returns(self):
        """
        TODO
        """
        self._check_fitted()
        return self.df[['returns', 'strategy']].sum().apply(np.exp)


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
        self.df['position'] = np.where(self.df['sma_fast'] > self.df['sma_slow'], 1, self.short_pos)
        self._dropna()

    def fit(self, fast=42, slow=252, metric='adj_close'):
        super().fit(**dict(fast=fast, slow=slow, metric=metric))

    def plot_moving_avgs(self, plt_kws=None):
        self._check_fitted()
        plt_kws = {} if plt_kws is None else plt_kws
        self.df[[self.metric, 'sma_fast', 'sma_slow']].dropna().plot(**plt_kws)


class Momentum(Strategy):
    """
    Todo
    """

    def _set_position(self):
        self.df['position'] = np.where(self.df['returns'].rolling(self.period).mean() > 0, 1, self.short_pos)
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
        self.df['position'] = np.where(self.df['distance'] > self.threshold, self.short_pos, np.nan)
        self.df['position'] = np.where(self.df['distance'] < -self.threshold, 1, self.df['position'])
        self.df['position'] = np.where(self.df['distance'] * self.df['distance'].shift(1) < 0, 0, self.df['position'])
        self.df['position'] = self.df['position'].ffill().fillna(0)
        self._dropna()

    def fit(self, sma=25, threshold=3.5, metric='adj_close'):
        super().fit(**dict(sma=sma, threshold=threshold, metric=metric))

    def plot_distance(self, plt_kws=None):
        self._check_fitted()
        plt_kws = {} if plt_kws is None else plt_kws
        self.df['distance'].dropna().plot(**plt_kws)
        plt.axhline(self.threshold, color='r')
        plt.axhline(-self.threshold, color='r')
        plt.axhline(0, color='k', linestyle='--')


class OLS(Strategy):
    """
    TODO
    """

    def fit(self, lags=5, metric='adj_close'):
        super().fit(**dict(lags=lags, metric=metric))

    def _set_lags(self):
        self.lag_cols = []
        for i in range(1, self.lags + 1):
            col = f'lag_{i}'
            self.lag_cols.append(col)
            self.df[col] = self.df['returns'].shift(i)
        self._dropna()

    def _set_position(self):
        self._set_lags()
        reg = np.linalg.lstsq(
            a=self.df[self.lag_cols],
            b=np.sign(self.df['returns']),
            rcond=None)[0]
        self.df['prediction'] = np.dot(self.df[self.lag_cols], reg)
        self.df['position'] = np.sign(self.df['prediction']).clip(lower=self.short_pos)

    def _set_strategy(self):
        self.df['strategy'] = self.df['returns'] * self.df['position']
