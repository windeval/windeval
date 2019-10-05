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

    @classmethod
    def ncep_ncar_2007(cls) -> float:
        """NCEP/NCAR from Köhl and Heimbach, 2007. [KH07]_

        .. math::

            C_d = 1.3 \\times 10^{-3}

        :return: Constant drag coefficient.

        Notes
        -----
        As of 2007 NCEP/NCAR used to use a constant drag coefficient as described
        in [KH07]_.

        """

        Cd = 1.3 * 1e-3

        return Cd

    @classmethod
    def large_and_pond_1981(cls, U: float) -> float:
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

        if 4 <= U and U < 11:
            Cd = 1.2 * 1e-3
        elif 11 <= U and U <= 25:
            Cd = (0.49 + 0.065 * U) * 1e-3
        else:
            raise ValueError(
                "Bulk-formula is not defined for values outside of the "
                + "interval I = [4, 25]"
            )

        return Cd

    @classmethod
    def yelland_and_taylor_1996(cls, U: float) -> float:
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

        if 3 <= U and U < 6:
            Cd = (0.29 + 3.1 / U + 7.7 / U ** 2) * 1e-3
        elif 6 <= U and U <= 26:
            Cd = (0.6 + 0.07 * U) * 1e-3
        else:
            raise ValueError(
                "Bulk-formula is not defined for values outside of the "
                + "interval I = [3, 26]"
            )

        return Cd

    @classmethod
    def kara_etal_2000(cls, V_a: float, T_s: float, T_a: float) -> float:
        """Kara et al., 2000. [K00]_

        .. math::

            \\begin{align}
            C_d =& C_{d0} + C_{d1} (T_s - T_a)\\\\
            C_{d0} =&
                (0.862 + 0.088 \\hat{V}_a - 0.00089 (\\hat{V}_a)^2) \\times 10^{-3}\\\\
            C_{d1} =&
                (0.1034 - 0.00678 \\hat{V}_a - 0.0001147 (\\hat{V}_a)^2) \\times 10^{-3}
            \\end{align}

        :param V_a: Absolute wind speed at 10 meter height.
        :param T_s: Sea surface temperature.
        :param T_a: Air temperature.
        :return: Drag coefficient.

        """

        V_hat_a = np.max([2.5, np.min([32.5, V_a])])

        C_d0 = (0.862 + 0.088 * V_hat_a - 0.00089 * V_hat_a ** 2) * 1e-3
        C_d1 = (0.1034 - 0.00678 * V_hat_a + 0.0001147 * V_hat_a ** 2) * 1e-3

        Cd = C_d0 + C_d1 * (T_s - T_a)

        return Cd

    @classmethod
    def trenberth_etal_1990(cls, U: float) -> float:
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
        if U <= 1:
            Cd = 2.18 * 1e-3
        elif 1 < U and U <= 3:
            Cd = (0.62 + 1.56 / U) * 1e-3
        elif 3 < U and U < 10:
            Cd = 1.14 * 1e-3
        else:
            Cd = (0.49 + 0.065 * U) * 1e-3

        return Cd

    @classmethod
    def large_and_yeager_2004(cls, U: float) -> float:
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

        if U == 0:
            raise ValueError("Bulk-formula is not defined for U = 0")
        else:
            Cd = (0.142 + 0.076 * U + 2.7 / U) * 1e-3

        return Cd
