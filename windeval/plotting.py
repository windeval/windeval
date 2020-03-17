import xarray as xr
from functools import singledispatch
from typing import Dict, Any, Union, List, Optional
import matplotlib.pyplot as plt


class Plot:
    @staticmethod
    def power_spectral_density(
        wnd: Dict[str, xr.Dataset], *args: Any, **kwargs: Dict[str, Any]
    ) -> None:
        for wndkey in wnd.keys():
            plt.semilogx(wnd[wndkey].power_spectral_density)

        plt.legend(wnd.keys())
        plt.title("PSD: power spectral density")
        plt.xlabel("Frequency")
        plt.ylabel("Power")
        plt.tight_layout()
        plt.grid()

        return None


@singledispatch
def plot(*args, **kwargs):
    raise NotImplementedError("Data type not supported for conversion.")


@plot.register
def _(
    wnddict: dict,
    var: str,
    *args: Any,
    dataset: Optional[Union[str, List[str]]] = None,
    **kwargs: Dict[str, Any]
) -> None:

    if dataset is None:
        dataset = []
    else:
        raise NotImplementedError(
            "Specifing a dataset for plots is not implemented yet."
        )

    if getattr(Plot, var, None) is not None:
        getattr(Plot, var)(wnddict, *dataset, *args, **kwargs)
    else:
        for wndkey in wnddict.keys():
            wnddict[wndkey][var].plot()

    return None
