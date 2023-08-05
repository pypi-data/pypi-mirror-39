# Helpful plotting utilities

import numpy as np
import matplotlib.pyplot as plt


def lineplot(x, y, ctr_type='mean', err_type='std', show_trials=False, **kwargs):
    """
    Plot the values with mean/median and std/95% CI/quartile as shading.
    This uses the automatic/default/preset color cycling for lines. Provided
    kwargs (including overriding color) will be passed to the line plotting

    The style is meant to match that produced by seaborn.lineplot, but on numpy
    arrays and with way less overhead (i.e., not putting it into a pandas
    dataframe and using the seaborn plotting). It doesn't support a lot of the
    fancy extras of its seaborn cousin.

    **Note:** This uses numpy's nan-functions (e.g., `nanmean` and `nanstd`) so
    your data can include nan values, and they will not contribute to summary
    statistic plots.

    Parameters
    ----------
    x : np.ndarray
        (n,) shape array of x-values to plot
    y : np.ndarray
        (m, n) shape array of y-values to plot, where m is the number of trials
    ctr_type : str, optional
        Which central statistic to plot is the primary summary metric. Options
        are 'mean' and 'median'. (the default is 'mean', which uses
        numpy.nanmean)
    err_type : str, optional
        Which error type to show for shading. Options are:
        - 'std': Standard deviation
        - '95ci': 95% confidence interval
        - 'quartile': [25%, 75%] confidence interval
        - None: No error plotting
        (the default is 'std', which is standard deviation)
    show_trials : bool, optional
        Whether or not to show plots of the individual trials (each row of y
        data). (the default is False, which means only summary data shown)
    """

    if ctr_type == 'mean':
        y_mid = np.nanmean(y, axis=0)
    elif ctr_type == 'median':
        y_mid = np.nanmedian(y, axis=0)

    show_err = True
    if err_type == 'std':
        std = np.nanstd(y, axis=0)
        err = np.array([y_mid-std, y_mid+std])
    elif err_type == '95ci':
        err = np.nanpercentile(y, [2.5, 97.5], axis=0)
    elif err_type == 'quartile':
        err = np.nanpercentile(y, [25, 75], axis=0)
    elif err_type is None:
        show_err = False
    else:
        raise ValueError("Invalid err_type")

    # Get the color the line should have by taking it from a dummy plot
    if 'color' not in kwargs:
        line, = plt.plot([], [])
        line_color = line.get_color()
        line.remove()
        # Add color to the existing kwargs
        kwargs['color'] = line_color
    plt.plot(x, y_mid, **kwargs)
    kwargs.pop('label', None)
    if show_err:
        plt.fill_between(x, err[0], err[1],  alpha=0.2, **kwargs)
    if show_trials:
        for trial in range(y.shape[0]):
            plt.plot(x, y[trial, :], linewidth=1, alpha=0.2)


if __name__ == '__main__':
    lineplot(np.arange(10), np.zeros([8, 10]))
