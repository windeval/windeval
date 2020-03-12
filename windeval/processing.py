"""Preprocessing module."""

import numpy as np
import xarray as xr
from typing import Callable, Union, Optional, Dict, Any


class BulkFormula:
    """Bulk formulas.

    **Currently available formulas:**

    * Large and Pond, 1981 [LP81]_
    * Trenberth et al., 1990 [T90]_
    * Yelland and Taylor, 1996 [YT96]_
    * Kara et al., 2000 [K00]_
    * Large and Yeager, 2004 [LY04]_
    * NCEP/NCAR (Köhl and Heimbach, 2007) [KH07]_

    Parameters
    ----------
    drag_coefficient : str
        Wind product data as Xarray-DataSet.
    bulk_formula : str
        Name of the zonal or meridional wind component as defined by the [CF]_ naming
        convention.

    Attributes
    ----------
    Cd : callable
        Drag coefficient selected by name from known definitions.
    calculate : callable
        Bulk formula selected by name from known definitions.

    References
    ----------
    .. [LP81]
        | Large and Pond, 1981.
        | `https://doi.org/10.1175/1520-0485(1981)011<0324:OOMFMI>2.0.CO;2`
    .. [T90]
        | Trenberth et al., 1990.
        | `https://doi.org/10.1175/1520-0485(1990)020<1742:TMACIG>2.0.CO;2`
    .. [YT96]
        | Yelland and Taylor, 1996.
        | `https://doi.org/10.1175/1520-0485(1996)026<0541:WSMFTO>2.0.CO;2`
    .. [K00]
        | Kara et al., 2000.
        | `https://doi.org/10.1175/1520-0426(2000)017<1421:EAABPO>2.0.CO;2`
    .. [LY04]
        | Large and Yeager, 2004.
        | `http://dx.doi.org/10.5065/D6KK98Q6`
    .. [KH07]
        | *A note on parameterizations of the drag coefficient*.
        | A. Köhl and P. Heimbach, August 15, 2007.
    .. [CF]
        | *CF Standard Name Table*.
        | http://cfconventions.org/Data/cf-standard-names/70/build/cf-standard-name-table.html


    """  # noqa: E501

    def __init__(
        self, drag_coefficient: str = "ncep_ncar_2007", bulk_formula: str = "generic"
    ):
        self.Cd: Callable[..., Union[xr.DataArray, np.ndarray]] = getattr(
            self, drag_coefficient.lower()
        )
        self.calculate: Callable[..., xr.DataArray] = getattr(
            self, bulk_formula.lower()
        )

    def generic(
        self, X: xr.Dataset, component: str, extend_ranges: Optional[bool] = None
    ) -> xr.DataArray:
        """Definition of generic bulk formula.

        .. math::

            \\tau = \\rho C_D \\mathopen|U\\mathclose| U

        Parameters
        ----------
        X : array_like
            Wind product data as Xarray-DataSet.
        component : str
            Name of the zonal or meridional wind component as defined by the CF_ naming
            convention.
        extend_ranges : bool, optional
            Fills undefined areas of the bulk formulas if `True`, returns `numpy.nan`
            values otherwise, defaults to defaults to wrapped function default.


        Returns
        -------
        array_like
            Wind stress.

        """
        d = {}
        for x in ["extend_ranges"]:
            if locals()[x] is None:
                continue
            d[x] = locals()[x]
        tau = (
            X.air_density
            * self.Cd(X, component, **d)
            * np.abs(X[component])
            * X[component]
        )

        return tau

    def ncep_ncar_2007(self, X: xr.Dataset, component: str) -> np.ndarray:
        """NCEP/NCAR from Köhl and Heimbach, 2007. [KH07]_

        .. math::

            C_d = 1.3 \\times 10^{-3}

        Parameters
        ----------
        X : array_like
            Wind product data as Xarray-DataSet.
        component : str
            Name of the zonal or meridional wind component as defined by the CF_ naming
            convention.

        Returns
        -------
        array_like
            Constant drag coefficient.

        Notes
        -----
        As of 2007 NCEP/NCAR used to use a constant drag coefficient as described
        in [KH07]_.

        """
        Cd = np.full(X[component].shape, 1.3e-3)

        return Cd

    def large_and_pond_1981(
        self, X: xr.Dataset, component: str, extend_ranges: bool = False
    ) -> xr.DataArray:
        """Large and Pond, 1981. [LP81]_

        .. math::

            \\begin{equation}
            C_d =
            \\begin{cases}
                1.2 \\times 10^{-3},&
                    \\text{if} \\quad 4 \\leq U \\lt 11\\\\
                (0.49 + 0.065 U) \\times 10^{-3},&
                    \\text{if} \\quad 11\\leq U\\leq 25\\\\
                \\text{undefined},& \\text{otherwise}
            \\end{cases}
            \\end{equation}

        Parameters
        ----------
        X : array_like
            Wind product data as Xarray-DataSet.
        component : str
            Name of the zonal or meridional wind component as defined by the CF_ naming
            convention.
        extend_ranges : bool, optional
            Retrun values outside of bulk formulas definition (`True`) or not (`False`),
            defaults to `False`.

        Returns
        -------
        array_like
            Drag coefficient.

        """
        Cd = 1.2e-3 * (X[component] < 11) + (0.49 + X[component] * 0.065) * 1e-3 * (
            X[component] > 11
        )
        if not extend_ranges:
            Cd = np.where(
                np.logical_and(4 <= X[component], X[component] <= 25), Cd, np.nan
            )

        return Cd

    def yelland_and_taylor_1996(
        self, X: xr.Dataset, component: str, extend_ranges: bool = False
    ) -> xr.DataArray:
        """Yelland and Taylor, 1996. [YT96]_

        .. math::

            \\begin{equation}
            C_d =
            \\begin{cases}
                (0.29 + \\frac{3.1}{U} + \\frac{7.7}{U^2}) \\times 10^{-3},&
                    \\text{if} \\quad 3 \\leq U \\lt 6\\\\
                (0.6 + 0.07 U) \\times 10^{-3},&
                    \\text{if} \\quad 6\\leq U\\leq 26\\\\
                \\text{undefined},& \\text{otherwise}
            \\end{cases}
            \\end{equation}

        Parameters
        ----------
        X : array_like
            Wind product data as Xarray-DataSet.
        component : str
            Name of the zonal or meridional wind component as defined by the CF_ naming
            convention.
        extend_ranges : bool, optional
            Retrun values outside of bulk formulas definition (`True`) or not (`False`),
            defaults to `False`.

        Returns
        -------
        array_like
            Drag coefficient.

        """
        epsilon = 1.0e-24
        Cd = (
            (
                0.29
                + 3.1 / (X[component] + epsilon)
                + (7.7 / ((X[component] + epsilon) ** 2))
            )
            * (X[component] < 6)
            * 1e-3
            + (0.6 + X[component] * 0.07) * (X[component] >= 6) * 1e-3
        )
        if not extend_ranges:
            Cd = np.where(
                np.logical_and(3 <= X[component], X[component] <= 26), Cd, np.nan
            )

        return Cd

    def kara_etal_2000(self, X: xr.Dataset, component: str) -> xr.DataArray:
        """Kara et al., 2000. [K00]_

        .. math::

            \\begin{align}
            C_d =& C_{d0} + C_{d1} (T_s - T_a)\\\\
            C_{d0} =&
                (0.862 + 0.088 \\hat{V}_a - 0.00089 (\\hat{V}_a)^2) \\times 10^{-3}\\\\
            C_{d1} =&
                (0.1034 - 0.00678 \\hat{V}_a - 0.0001147 (\\hat{V}_a)^2) \\times 10^{-3}
            \\end{align}

        .. math::

            \\hat{V}_a = \\text{max}(2.5, \\text{min}(32.5, V_a))

        Parameters
        ----------
        X : array_like
            Wind product data as Xarray-DataSet.
        component : str
            Name of the zonal or meridional wind component as defined by the CF_ naming
            convention.

        Returns
        -------
        array_like
            Drag coefficient.

        """
        V_hat_a = np.maximum(2.5, np.minimum(32.5, X[component]))
        C_d0 = (0.862 + 0.088 * V_hat_a - 0.00089 * V_hat_a ** 2) * 1e-3
        C_d1 = (0.1034 - 0.00678 * V_hat_a + 0.0001147 * V_hat_a ** 2) * 1e-3
        Cd = C_d0 + C_d1 * (X.sea_surface_temperature - X.air_temperature)

        return Cd

    def trenberth_etal_1990(self, X: xr.Dataset, component) -> xr.DataArray:
        """Trenberth, Large and Olson, 1990. [T90]_

        .. math::

            \\begin{equation}
            C_d =
            \\begin{cases}
                2.18 \\times 10^{-3},& \\text{if} \\quad U\\leq 1\\\\
                (0.62 + \\frac{1.56}{U}) \\times 10^{-3},&
                    \\text{if} \\quad 1 \\lt U\\leq 3\\\\
                1.14 \\times 10^{-3},&
                    \\text{if} \\quad 3 \\lt U\\lt 10\\\\
                (0.49 + 0.065 U) \\times 10^{-3},&
                    \\text{otherwise}
            \\end{cases}
            \\end{equation}

        Parameters
        ----------
        X : array_like
            Wind product data as Xarray-DataSet.
        component : str
            Name of the zonal or meridional wind component as defined by the CF_ naming
            convention.

        Returns
        -------
        array_like
            Drag coefficient.

        Notes
        -----
        Possibly not exactly Trenberth et al., 1990 [T90]_, at a glance there are
        some differences to the current implementation.

        """
        epsilon = 1.0e-24
        Cd = (
            2.18e-3 * (X[component] <= 1)
            + (0.62 + 1.56 / (X[component] + epsilon))
            * 1.0e-3
            * np.logical_and(1 < X[component], X[component] <= 3)
            + 1.14e-3 * np.logical_and(3 < X[component], X[component] < 10)
            + (0.49 + X[component] * 0.065) * 1.0e-3 * (10 <= X[component])
        )

        return Cd

    def large_and_yeager_2004(
        self, X: xr.Dataset, component: str, extend_ranges: bool = False
    ) -> xr.DataArray:
        """Large and Yeager, 2004. [LY04]_

        .. math::

            \\begin{equation}
            C_d =
            \\begin{cases}
                \\text{undefined},& \\text{if} \\quad U = 0\\\\
                (0.142 + 0.076 U + \\frac{2.7}{U}) \\times 10^{-3},& \\text{otherwise}
            \\end{cases}
            \\end{equation}

        Parameters
        ----------
        X : array_like
            Wind product data as Xarray-DataSet.
        component : str
            Name of the zonal or meridional wind component as defined by the CF_ naming
            convention.
        extend_ranges : bool, optional
            Retrun values outside of bulk formulas definition (`True`) or not (`False`),
            defaults to `False`.

        Returns
        -------
        array_like
            Drag coefficient.

        """
        epsilon = 1.0e-24
        Cd = ((0.142 + X[component] * 0.076 + 2.7 / (X[component] + epsilon))) * 1e-3
        if not extend_ranges:
            Cd = np.where((X[component] != 0), Cd, np.nan)

        return Cd


def wind_speed(X: xr.Dataset) -> xr.Dataset:
    """Calculate absolut windspeed from U and V.

    Notes
    -----
    Spatial distances of U and V grid points are not taken into account.

    .. math::

        s = \\sqrt{u^2 + v^2}

    Parameters
    ----------
    X : array_like
        Wind product data as Xarray-DataSet.

    Returns
    -------
    array_like
        Absolute wind speed.

    """
    X["wind_speed"] = np.sqrt(
        np.power(X.data_vars["eastward_wind"], 2)
        + np.power(X.data_vars["northward_wind"], 2)
    )

    return X


def surface_downward_eastward_stress(
    X: xr.Dataset,
    drag_coefficient: Optional[str] = None,
    bulk_formula: Optional[str] = None,
    extend_ranges: Optional[bool] = None,
) -> xr.Dataset:
    """Caclulate surface downward eastward stress.

    Parameters
    ----------
    X : array_like
        Wind product data as Xarray-DataSet.
    drag_coefficient : str, optional
        Name of drag coefficient method, defaults to :meth:`windeval.BulkFormula`'s
        default.
    bulk_formula : str, optional
        Name of bulk formula method, defaults to :meth:`windeval.BulkFormula`'s default.

    Returns
    -------
    array_like
        Surface downward eastward stress.

    """
    X["surface_downward_eastward_stress"] = BulkFormula(
        *[s for s in [drag_coefficient, bulk_formula] if s is not None]
    ).calculate(X, "eastward_wind", *[s for s in [extend_ranges] if s is not None])

    return X


def surface_downward_northward_stress(
    X: xr.Dataset,
    drag_coefficient: Optional[str] = None,
    bulk_formula: Optional[str] = None,
    extend_ranges: Optional[bool] = None,
) -> xr.Dataset:
    """Caclulate surface downward northward stress.

    Parameters
    ----------
    X : array_like
        Wind product data as Xarray-DataSet.
    drag_coefficient : str, optional
        Name of drag coefficient method, defaults to :meth:`windeval.BulkFormula`'s
        default.
    bulk_formula : str, optional
        Name of bulk formula method, defaults to :meth:`windeval.BulkFormula`'s default.

    Returns
    -------
    array_like
        Surface downward northward stress.

    """
    X["surface_downward_northward_stress"] = BulkFormula(
        *[s for s in [drag_coefficient, bulk_formula] if s is not None]
    ).calculate(X, "northward_wind", *[s for s in [extend_ranges] if s is not None])

    return X


def northward_ekman_transport(X: xr.Dataset) -> xr.Dataset:
    """Calculate meridional Ekman transport.

    .. math::

        M_y = -\\frac{\\tau_x}{f}

    Parameters
    ----------
    X : array_like
        Wind product data as Xarray-DataSet.

    Returns
    -------
    array_like
        Northward Ekman transport.

    """
    _has(X, "surface_downward_eastward_stress")

    X[
        "northward_ekman_transport"
    ] = -X.surface_downward_eastward_stress / _Coriolis().parameter(X.latitude)

    return X


def eastward_ekman_transport(X: xr.Dataset) -> xr.Dataset:
    """Calculate zonal Ekman transport.

    .. math::

        M_x = \\frac{\\tau_y}{f}

    Parameters
    ----------
    X : array_like
        Wind product data as Xarray-DataSet.

    Returns
    -------
    array_like
        Eastward Ekman transport.

    """
    _has(X, "surface_downward_northward_stress")

    X[
        "eastward_ekman_transport"
    ] = X.surface_downward_northward_stress / _Coriolis().parameter(X.latitude)

    return X


class _Coriolis:
    def __init__(self):
        self.c = 2 * 2 * np.pi / ((23 * 60 + 56) * 60 + 4.1)

    def parameter(self, y: xr.DataArray) -> xr.DataArray:
        f = self.c * np.sin(np.deg2rad(y))

        return f

    def derivative(self, y: xr.DataArray) -> xr.DataArray:
        b = self.c * np.cos(np.deg2rad(y))

        return b


def _has(X: xr.Dataset, v: str) -> None:
    """Calculate variable `v` if missing in `X`.

    Uses function defaults for calculations.

    """
    if v not in X.data_vars.keys():
        globals()[v](X)

    return None


def sverdrup_transport(X: xr.Dataset) -> xr.Dataset:
    """Calculate Sverdrup transport.

    .. math::

        V = \\hat{\\mathbf{k}} \\cdot \\frac{\\mathbf{\\nabla}\\times\\tau}{\\beta}

    Parameters
    ----------
    X : array_like
        Wind product data as Xarray-DataSet.

    Returns
    -------
    array_like
        Sverdrup transport.

    """
    _has(X, "surface_downward_eastward_stress")
    _has(X, "surface_downward_northward_stress")

    def mesh(X, M):
        dims = [x for x in list(X.coords) if x not in ["longitude", "latitude"]]
        for d in dims:
            M = np.multiply.outer(np.ones(len(X.coords[d])), M)

        return M

    X["sverdrup_transport"] = (
        [x for x in reversed(list(X.coords))],
        np.full(X.surface_downward_northward_stress.shape, np.nan),
    )

    lon = mesh(
        X,
        np.outer(
            np.ones(-1 + len(X.coords["latitude"])),
            X.longitude.values[1:] - X.longitude.values[:-1],
        ),
    )
    lat = mesh(
        X,
        np.outer(
            X.latitude.values[1:] - X.latitude.values[:-1],
            np.ones(-1 + len(X.coords["longitude"])),
        ),
    )

    X["sverdrup_transport"][..., :-1, :-1] = (
        (
            X.surface_downward_northward_stress[..., 1:, :-1].values
            - X.surface_downward_northward_stress[..., :-1, :-1].values
        )
        / lon
        - (
            X.surface_downward_eastward_stress[..., :-1, 1:].values
            - X.surface_downward_eastward_stress[..., :-1, :-1].values
        )
        / lat
    ) / _Coriolis().derivative(lat)

    return X


def conversions(
    wndpr: Dict[str, xr.Dataset], *args: Any, **kwargs: Dict[str, Any]
) -> Dict[str, xr.Dataset]:
    raise NotImplementedError("Conversions are not yet implemented.")


def diagnostics(
    wndpr: Dict[str, xr.Dataset], *args: Any, **kwargs: Dict[str, Any]
) -> Dict[str, xr.Dataset]:
    raise NotImplementedError("Diagnostics are not yet implemented.")
