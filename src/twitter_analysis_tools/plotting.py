import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set(style="whitegrid", font_scale=1.5, context="talk")

"""
For details on the params below, see the matplotlib docs:
https://matplotlib.org/users/customizing.html
"""

plt.rcParams["axes.edgecolor"] = "0.6"
plt.rcParams["figure.dpi"] = 200
plt.rcParams["font.family"] = "serif"
plt.rcParams["grid.color"] = "0.85"
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["legend.columnspacing"] *= 0.8
plt.rcParams["legend.edgecolor"] = "0.6"
plt.rcParams["legend.markerscale"] = 1.0
plt.rcParams["legend.framealpha"] = "1"
plt.rcParams["legend.handlelength"] *= 1.5
plt.rcParams["legend.numpoints"] = 2
plt.rcParams["text.usetex"] = True
plt.rcParams["xtick.major.pad"] = -3
plt.rcParams["ytick.major.pad"] = -2


def plot_data(
    data,
    x=None,
    plot_type="lineplot",
    filepath=None,
    save_fig=True,
    figsize=[12.0, 6.0],
):
    """
    Args:
        data (2d array): 2d array with dimensions: num_topics x num_time_slices

    Examples:

        A simple example.

        >>> import numpy as np
        >>> data = np.arange(40).reshape([4,10])
        >>> plot_data(data, save_fig=False)
        >>> plot_data(data, plot_type='lineplot', save_fig=False)
        >>> plot_data(data, plot_type='stackplot', save_fig=False)

        An example using a Pipeline.

        >>> import numpy as np
        >>> from functools import partial
        >>> from covid19.utils import Pipeline
        >>> data = [i*np.arange(10).T for i in range(1, 20)]
        >>> data_pipeline = Pipeline(data)
        >>> data_pipeline = data_pipeline.add_map(partial(np.expand_dims, axis=1))
        >>> topic_distributions = np.concatenate(list(data_pipeline), axis=1)
        >>> plot_data(topic_distributions, plot_type='stackplot', save_fig=False)
        >>> plot_data(topic_distributions, plot_type='lineplot', save_fig=False)
    """
    # Get dimensions.
    num_topics, num_time_slices = data.shape
    sns.set_palette(sns.husl_palette(num_topics))

    # Create labels.
    # TODO: pass labels in as argument.
    labels = ["Topic {}".format(i) for i in range(1, num_topics + 1)]

    if x is None:
        x = np.arange(num_time_slices)

    # Plot
    fig = plt.figure(figsize=figsize)

    # Plot data.
    if plot_type == "lineplot":
        for topic in range(num_topics):
            plt.plot(x, data[topic, :], label=labels[topic])
    if plot_type == "stackplot":
        plt.stackplot(x, data, labels=labels)

    # Put the legend out of the figure
    plt.legend(
        bbox_to_anchor=(1.05, 0.5),
        loc="center left",
        borderaxespad=0.0,
        prop={"size": 10},
    )

    plt.xticks(rotation=45)

    if save_fig:
        if filepath is None:
            raise Exception("Filepath must be specified if save_fig=True.")
        fig.savefig(filepath + ".svg", bbox_inches="tight", transparent=True)
        fig.savefig(filepath + ".png", bbox_inches="tight", transparent=True)
    plt.close()
