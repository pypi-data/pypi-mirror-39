__all__ = ['calibrate_arrays',
           'estimate_baseline',
           'estimate_commonmode',
           'make_continuummap']


# standard library
from logging import getLogger
logger = getLogger(__name__)


# dependent packages
import numpy as np
import xarray as xr
import decode as dc
import defunc as fn
from scipy.interpolate import interp1d
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import TruncatedSVD


# module constants


def calibrate_arrays(Pon, Poff, Pr, Tamb=273.0):
    """Apply R-SKY intensity calibration to De:code arrays.

    Args:
        Pon (xarray.DataArray): De:code array of ON point.
        Poff (xarray.DataArray): De:code array of OFF point.
        Pr (xarray.DataArray): De:code array of R measurement.

    Returns:
        Ton (xarray.DataArray): Calibrated De:code array of ON point.
        Toff (xarray.DataArray): Calibrated De:code array of OFF point.

    """
    Ton  = _calculate_Ton(Pon, Poff, Pr, Tamb)
    Toff = _calculate_Toff(Poff, Pr, Tamb)

    return Ton, Toff


@fn.foreach_onref
def _calculate_Ton(Pon, Poff, Pr, Tamb):
    offids = np.unique(Poff.scanid)
    assert len(offids) == 2

    Poff_f = Poff[Poff.scanid == offids[0]] # former
    Poff_l = Poff[Poff.scanid == offids[1]] # latter

    ton    = Pon.time.astype(float).values
    toff_f = Poff_f.time.astype(float).values
    toff_l = Poff_l.time.astype(float).values
    toff   = np.array([toff_f.mean(), toff_l.mean()])
    spec   = np.array([Poff_f.mean('t'), Poff_l.mean('t')])

    Poff_ip = interp1d(toff, spec, axis=0)(ton)
    Pr_0 = Pr.mean('t').values

    return Tamb * (Pon-Poff_ip) / (Pr_0-Poff_ip)


@fn.foreach_scanid
def _calculate_Toff(Poff, Pr, Tamb):
    Poff_0 = Poff.mean('t').values
    Pr_0 = Pr.mean('t').values

    return Tamb * (Poff-Poff_0) / (Pr_0-Poff_0)


def estimate_baseline(Ton, Tamb=273.0, order=0, weight=None,
                      model='LinearRegression', **kwargs):
    """Estimate ultra-wideband baseline.

    Args:
        Ton (xarray.DataArray): Calibrated De:code array of ON point.
        Tamb (float, optional): Ambient temperature used in calibration.
        order (int, optional): Maximum order of a polynomial function
            which is assumed to represent a continuum emission spectrum.
            Default is 0 (flat continuum emission).
        weight (array, int, or float, optional): 1D weight along ch axis.
            If it is a number, then slope**<number> is used instead.
            It is only for `model` = 'LinearRegression' or 'Ridge'
            (ignored otherwise). Default is None (uniform weight).
        model (str, optional): Model name of `sklearn.linear_model`.
            Default is 'LinearRegression' (least squares linear regression).
        kwargs (dict, optional): Keyword arguments for model initialization.

    Returns:
        Tbase (xarray.DataArray): De:code array of estimated baseline.

    """
    freq = np.asarray(Ton.kidfq)
    slope = _calculate_dtau_dpwv(freq)

    X = np.zeros([len(freq), order+1])
    X[:, -1] = Tamb*slope
    for i in range(order):
        X[:, i] = freq**(i+1)

    y = Ton.values.T

    if weight is None:
        weight = np.ones_like(slope)
    elif isinstance(weight, (int, float)):
        weight = slope**weight
    else:
        weight = np.asarray(weight)

    if model in ['LinearRegression', 'Ridge']:
        model = getattr(linear_model, model)(**kwargs)
        model.fit(X, y, sample_weight=weight)
    else:
        model = getattr(linear_model, model)(**kwargs)
        model.fit(X, y)

    Tbase = np.outer(model.coef_[:, -1], X[:, -1])
    Tbase = dc.full_like(Ton, Tbase)
    Tbase.attrs['model'] = model
    Tbase.attrs['X'] = X
    Tbase.attrs['y'] = y
    Tbase.attrs['weight'] = weight
    return Tbase


def _calculate_dtau_dpwv(freq):
    df = fn.read_atm(kind='tau')
    df = df.loc[freq.min()-0.1:freq.max()+0.1].T

    model = LinearRegression()
    model.fit(df.index[:,None], df)

    freq_ = df.columns.copy()
    coef_ = model.coef_.T[0]
    return interp1d(freq_, coef_)(freq)


@fn.foreach_onref
def estimate_commonmode(Ton, Toff):
    """Estimate common-mode noises by PCA.

    Args:
        Ton (xarray.DataArray): Calibrated De:code array of ON point.
        Toff (xarray.DataArray): Calibrated De:code array of OFF point.

    Returns:
        Tcom (xarray.DataArray): De:code array of estimated common-mode.

    """
    Xon  = fn.normalize(Ton)
    Xoff = fn.normalize(Toff)

    model = TruncatedSVD(n_components)
    model.fit(Xoff)
    P = model.components_
    C = model.transform(Xon)

    Xcom = dc.full_like(Xon, C@P)
    return fn.denormalize(Xcom)


def make_continuummap(cube, weight=None):
    """Make continuum map from cube.

    Args:
        cube (xarray.DataArray): De:code cube to be processed.
        weight (xarray.DataArray, optional): Weight cube.
            If not spacified, then `cube.noise**-2` is used.

    Returns:
        contmap (xarray.DataArray): Continuum map.

    """
    fn.assert_isdcube(cube)

    if weight is None:
        weight = cube.noise**-2

    return (cube*weight).sum('ch') / weight.sum('ch')