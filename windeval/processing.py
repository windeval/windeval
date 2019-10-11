"""Preprocessing module."""

import numpy as np


class BulkFormula:
    """Example for bulk formula integration.

    **Currently available formulas**

    * Large and Pond, 1981 [LP81]_
    * Trenberth et al., 1990 [T90]_
    * Yelland and Taylor, 1996 [YT96]_
    * Kara et al., 2000 [K00]_
    * Large and Yeager, 2004 [LY04]_
    * NCEP/NCAR (Köhl and Heimbach, 2007) [KH07]_


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

    """

    def __init__(
        self, drag_coefficient: str = "ncep_ncar_2007", bulk_formula: str = "generic"
    ):
        self.Cd = getattr(self, drag_coefficient.lower())
        self.calculate = getattr(self, bulk_formula.lower())

    def generic(self, **kwargs) -> np.ndarray:
        """Definition of generic bulk formula.

        .. math::

            \\tau = \\rho C_D \\mathopen|\\Delta U\\mathclose| \\Delta U

        :return: Wind stress.

        """
        rho = kwargs.pop("rho")
        u = kwargs.pop("u")
        return rho * self.Cd(**kwargs) * kwargs["U"] * u

    def ncep_ncar_2007(self, U: np.ndarray = np.ndarray) -> np.ndarray:
        """NCEP/NCAR from Köhl and Heimbach, 2007. [KH07]_

        .. math::

            C_d = 1.3 \\times 10^{-3}

        :return: Constant drag coefficient.

        Notes
        -----
        As of 2007 NCEP/NCAR used to use a constant drag coefficient as described
        in [KH07]_.

        """

        Cd = np.empty(U.shape)
        Cd.fill(1.3e-3)

        return Cd

    def large_and_pond_1981(self, U: np.ndarray = np.ndarray) -> np.ndarray:
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

        :param U: Absolute wind speed at 10 meter height.
        :return: Drag coefficient.

        """

        Cd = np.empty(U.shape)
        Cd.fill(np.nan)

        interval1 = np.logical_and(4 <= U, U < 11)
        interval2 = np.logical_and(11 <= U, U <= 25)

        Cd[interval1] = 1.2e-3
        Cd[interval2] = (0.49 + 0.065 * U[interval2]) * 1e-3

        return Cd

    def yelland_and_taylor_1996(self, U: np.ndarray = np.ndarray) -> np.ndarray:
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

        :param U: Absolute wind speed at 10 meter height.
        :return: Drag coefficient.

        """

        Cd = np.empty(U.shape)
        Cd.fill(np.nan)

        interval1 = np.logical_and(3 <= U, U < 6)
        interval2 = np.logical_and(6 <= U, U <= 26)

        Cd[interval1] = (0.29 + 3.1 / U[interval1] + 7.7 / U[interval1] ** 2) * 1e-3
        Cd[interval2] = (0.6 + 0.07 * U[interval2]) * 1e-3

        return Cd

    def kara_etal_2000(
        self,
        U: np.ndarray = np.ndarray,
        T_a: np.ndarray = np.ndarray,
        T_s: np.ndarray = np.ndarray,
    ) -> np.ndarray:
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

        :param U: (V_a) Absolute wind speed at 10 meter height.
        :param T_s: Sea surface temperature.
        :param T_a: Air temperature.
        :return: Drag coefficient.

        """

        # naming according to source
        V_a = U
        V_hat_a = np.maximum(2.5, np.minimum(32.5, V_a))

        C_d0 = (0.862 + 0.088 * V_hat_a - 0.00089 * V_hat_a ** 2) * 1e-3
        C_d1 = (0.1034 - 0.00678 * V_hat_a + 0.0001147 * V_hat_a ** 2) * 1e-3

        Cd = C_d0 + C_d1 * (T_s - T_a)

        return Cd

    def trenberth_etal_1990(self, U: np.ndarray = np.ndarray) -> np.ndarray:
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

        :param U: Absolute wind speed at 10 meter height.
        :return: Drag coefficient.

        Notes
        -----
        Possibly not exactly Trenberth et al., 1990 [T90]_, at a glance there are
        some differences to the current implementation.

        """

        Cd = np.empty(U.shape)
        Cd.fill(np.nan)

        interval1 = U <= 1
        interval2 = np.logical_and(1 < U, U <= 3)
        interval3 = np.logical_and(3 < U, U < 10)
        interval4 = 10 <= U

        Cd[interval1] = 2.18e-3
        Cd[interval2] = (0.62 + 1.56 / U[interval2]) * 1e-3
        Cd[interval3] = 1.14e-3
        Cd[interval4] = (0.49 + 0.065 * U[interval4]) * 1e-3

        return Cd

    def large_and_yeager_2004(self, U: np.ndarray = np.ndarray) -> np.ndarray:
        """Large and Yeager, 2004. [LY04]_

        .. math::

            \\begin{equation}
            C_d =
            \\begin{cases}
                \\text{undefined},& \\text{if} \\quad U = 0\\\\
                (0.142 + 0.076 U + \\frac{2.7}{U}) \\times 10^{-3},& \\text{otherwise}
            \\end{cases}
            \\end{equation}

        :param U: Absolute wind speed at 10 meter height.
        :return: Drag coefficient.

        """

        Cd = np.empty(U.shape)
        Cd.fill(np.nan)

        interval1 = U != 0

        Cd[interval1] = (0.142 + 0.076 * U[interval1] + 2.7 / U[interval1]) * 1e-3

        return Cd
