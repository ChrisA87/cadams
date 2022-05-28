import pytest
import pandas as pd
import numpy as np
from app.models.trading import SMA, Momentum, MeanReversion
from app.models.errors import NotFittedError


@pytest.fixture
def mock_stock_price_df():
    np.random.seed(0)
    yield pd.DataFrame({
        'date': pd.date_range('2018-01-01', freq='D', periods=1000),
        'adj_close': np.random.randn(1000),
        'open': np.random.randn(1000)
    })


@pytest.mark.parametrize('method', ['plot_moving_avgs', 'plot_position', 'plot_strategy'])
def test_sma_not_fitted_raises_error(mock_stock_price_df, method):
    sma = SMA(mock_stock_price_df)
    assert sma.__repr__() == '<SMA>'
    with pytest.raises(NotFittedError):
        getattr(sma, method)()


@pytest.mark.parametrize('expected_col', ['sma_slow', 'sma_fast', 'strategy', 'position', 'returns'])
def test_sma_fitted_has_expected_columns(mock_stock_price_df, expected_col):
    sma = SMA(mock_stock_price_df)
    sma.fit()
    assert sma.__repr__() == '<SMA fitted>'
    assert expected_col in sma.df.columns


@pytest.mark.parametrize('expected_col', ['strategy', 'position', 'returns'])
def test_momentum_fitted_has_expected_columns(mock_stock_price_df, expected_col):
    momentum = Momentum(mock_stock_price_df)
    momentum.fit()
    assert momentum.__repr__() == '<Momentum fitted>'
    assert expected_col in momentum.df.columns


@pytest.mark.parametrize('expected_col', ['strategy', 'position', 'returns', 'sma', 'distance'])
def test_meanreversion_fitted_has_expected_columns(mock_stock_price_df, expected_col):
    mr = MeanReversion(mock_stock_price_df)
    mr.fit()
    assert mr.__repr__() == '<MeanReversion fitted>'
    assert expected_col in mr.df.columns


@pytest.mark.parametrize('fast, slow', [(15, 15), (15, 10)])
def test_sma_fast_greater_than_slow_raises_ValueError(mock_stock_price_df, fast, slow):
    sma = SMA(mock_stock_price_df)
    with pytest.raises(ValueError):
        sma.fit(fast=fast, slow=slow)


@pytest.mark.parametrize('method', ['plot_moving_avgs', 'plot_position', 'plot_strategy'])
def test_plotting_methods_on_fitted_sma(mock_stock_price_df, method):
    sma = SMA(mock_stock_price_df)
    sma.fit()
    assert getattr(sma, method)() is None


@pytest.mark.parametrize('method', ['plot_distance', 'plot_position', 'plot_strategy'])
def test_plotting_methods_on_fitted_mean_reversion(mock_stock_price_df, method):
    mr = MeanReversion(mock_stock_price_df)
    mr.fit()
    assert getattr(mr, method)() is None


def test_no_date_raises_KeyError(mock_stock_price_df):
    df = mock_stock_price_df.drop('date', axis=1)
    with pytest.raises(KeyError):
        SMA(df)


def test_get_plot_title_with_no_stock_is_none(mock_stock_price_df):
    assert SMA(mock_stock_price_df)._get_plot_title(None) is None
