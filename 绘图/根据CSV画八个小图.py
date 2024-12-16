#!/user/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import matplotlib.pyplot as plt
# from ultralytics.utils import LOGGER

def plot_results(file='path/to/results.csv', dir='', on_plot=None):
    """
    Plot training results from a results CSV file. The function supports various types of data including segmentation,
    pose estimation, and classification. Plots are saved as 'results.png' in the directory where the CSV is located.

    Args:
        file (str, optional): Path to the CSV file containing the training results. Defaults to 'path/to/results.csv'.
        dir (str, optional): Directory where the CSV file is located if 'file' is not provided. Defaults to ''.
        segment (bool, optional): Flag to indicate if the data is for segmentation. Defaults to False.
        pose (bool, optional): Flag to indicate if the data is for pose estimation. Defaults to False.
        classify (bool, optional): Flag to indicate if the data is for classification. Defaults to False.
        on_plot (callable, optional): Callback function to be executed after plotting. Takes filename as an argument.
            Defaults to None.

    Example:
        ```python
        from ultralytics.utils.plotting import plot_results

        plot_results('path/to/results.csv', segment=True)
        ```
    """
    import pandas as pd
    from scipy.ndimage import gaussian_filter1d
    save_dir = Path(file).parent if file else Path(dir)

    fig, ax = plt.subplots(2, 5, figsize=(12, 6), tight_layout=True)
    index = [1, 2, 3, 4, 5, 8, 9, 10, 6, 7]
    ax = ax.ravel()
    files = list(save_dir.glob('results*.csv'))
    assert len(files), f'No results.csv files found in {save_dir.resolve()}, nothing to plot.'
    for f in files:
        try:
            data = pd.read_csv(f)
            s = [x.strip() for x in data.columns]
            x = data.values[:, 0]
            for i, j in enumerate(index):
                y = data.values[:, j].astype('float')
                # y[y == 0] = np.nan  # don't show zero values
                ax[i].plot(x, y, marker='.', label=f.stem, linewidth=2, markersize=8)  # actual results
                ax[i].plot(x, gaussian_filter1d(y, sigma=3), ':', label='smooth', linewidth=2)  # smoothing line
                ax[i].set_title(s[j], fontsize=13)
                # ax[i].set_xlabel( fontsize=8)
                # ax[i].set_ylabel( fontsize=8)

                # if j in [8, 9, 10]:  # share train and val loss y axes
                #     ax[i].get_shared_y_axes().join(ax[i], ax[i - 5])
        except Exception as e:
            # LOGGER.warning(f'WARNING: Plotting error for {f}: {e}')
            print('Hhaa')
    ax[1].legend()

    # fname = save_dir / 'results.png'
    plt.show()
    # fig.savefig(fname, dpi=200)
    # plt.close()
    # if on_plot:
    #     on_plot(fname)


plot_results(r"C:\Users\yyj\OneDrive\桌面\论文相关\结果\预训练后50轮\ACA_LKA_obb\results.csv")

