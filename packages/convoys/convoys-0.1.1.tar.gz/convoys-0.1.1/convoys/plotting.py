import numpy
from matplotlib import pyplot
import convoys.multi

__all__ = ['plot_cohorts']


_models = {
    'kaplan-meier': lambda ci: convoys.multi.KaplanMeier(),
    'exponential': lambda ci: convoys.multi.Exponential(ci=ci),
    'weibull': lambda ci: convoys.multi.Weibull(ci=ci),
    'gamma': lambda ci: convoys.multi.Gamma(ci=ci),
    'generalized-gamma': lambda ci: convoys.multi.GeneralizedGamma(ci=ci),
}


def plot_cohorts(G, B, T, t_max=None, model='kaplan-meier',
                 ci=None, plot_kwargs={}, plot_ci_kwargs={}, groups=None):
    # Set x scale
    if t_max is None:
        _, t_max = pyplot.gca().get_xlim()
        t_max = max(t_max, max(T))

    if groups is None:
        groups = set(G)

    # Fit model
    m = _models[model](ci=bool(ci))
    m.fit(G, B, T)

    # Plot
    colors = pyplot.get_cmap('tab10').colors
    colors = [colors[i % len(colors)] for i in range(len(groups))]
    t = numpy.linspace(0, t_max, 1000)
    _, y_max = pyplot.gca().get_ylim()
    for j, (group, color) in enumerate(zip(groups, colors)):
        n = sum(1 for g in G if g == j)  # TODO: slow
        k = sum(1 for g, b in zip(G, B) if g == j and b)  # TODO: slow
        label = '%s (n=%.0f, k=%.0f)' % (group, n, k)

        if ci is not None:
            p_y, p_y_lo, p_y_hi = m.cdf(j, t, ci=ci).T
            pyplot.fill_between(t, 100. * p_y_lo, 100. * p_y_hi,
                                color=color, alpha=0.2, **plot_ci_kwargs)
        else:
            p_y = m.cdf(j, t).T
        pyplot.plot(t, 100. * p_y, color=color, linewidth=1.5,
                    alpha=0.7, label=label, **plot_kwargs)

        y_max = max(y_max, 110. * max(p_y))

    pyplot.xlim([0, t_max])
    pyplot.ylim([0, y_max])
    pyplot.ylabel('Conversion rate %')
    pyplot.gca().grid(True)
    return m
