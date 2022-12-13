from __future__ import annotations

import typing

from ..doctools import document
from .geom import geom
from .geom_linerange import geom_linerange
from .geom_path import geom_path
from .geom_point import geom_point

if typing.TYPE_CHECKING:
    import types
    from typing import Any

    import matplotlib as mpl
    import pandas as pd

    import plotnine as p9


@document
class geom_pointrange(geom):
    """
    Vertical interval represented by a line with a point

    {usage}

    Parameters
    ----------
    {common_parameters}
    fatten : float, optional (default: 2)
        A multiplicative factor used to increase the size of the
        point along the line-range.
    """

    DEFAULT_AES = {'alpha': 1, 'color': 'black', 'fill': None,
                   'linetype': 'solid', 'shape': 'o', 'size': 0.5}
    REQUIRED_AES = {'x', 'y', 'ymin', 'ymax'}
    DEFAULT_PARAMS = {'stat': 'identity', 'position': 'identity',
                      'na_rm': False, 'fatten': 4}

    @staticmethod
    def draw_group(
        data: pd.DataFrame,
        panel_params: types.SimpleNamespace,
        coord: p9.coords.coord.coord,
        ax: mpl.axes.Axes,
        **params: Any
    ) -> None:
        geom_linerange.draw_group(data.copy(), panel_params,
                                  coord, ax, **params)
        data['size'] = data['size'] * params['fatten']
        data['stroke'] = geom_point.DEFAULT_AES['stroke']
        geom_point.draw_group(data, panel_params, coord, ax, **params)

    @staticmethod
    def draw_legend(
        data: pd.DataFrame,
        da: mpl.patches.DrawingArea,
        lyr: p9.layer.layer
    ) -> mpl.patches.DrawingArea:
        """
        Draw a point in the box

        Parameters
        ----------
        data : dataframe
        da : DrawingArea
        lyr : layer

        Returns
        -------
        out : DrawingArea
        """
        assert lyr.geom is not None
        geom_path.draw_legend(data, da, lyr)
        data['size'] = data['size'] * lyr.geom.params['fatten']
        data['stroke'] = geom_point.DEFAULT_AES['stroke']
        geom_point.draw_legend(data, da, lyr)
        return da
