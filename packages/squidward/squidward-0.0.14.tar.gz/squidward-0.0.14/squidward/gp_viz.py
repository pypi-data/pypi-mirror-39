import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from squidward.utils import make_grid, atmost_1d

class regression:
    def plot_1d(x, mean, var):
        x = atmost_1d(x)
        mean = atmost_1d(mean)
        var = atmost_1d(var)

        plt.fill_between(x,
                     mean-.674*np.sqrt(var),
                     mean+.674*np.sqrt(var),
                     color='k', alpha=.4, label='50% Credible Interval')
        plt.fill_between(x,
                     mean-1.150*np.sqrt(var),
                     mean+1.150*np.sqrt(var),
                     color='k', alpha=.3, label='75% Credible Interval')
        plt.fill_between(x,
                     mean-1.96*np.sqrt(var),
                     mean+1.96*np.sqrt(var),
                     color='k', alpha=.2, label='95% Credible Interval')
        plt.fill_between(x,
                     mean-2.326*np.sqrt(var),
                     mean+2.326*np.sqrt(var),
                     color='k', alpha=.1, label='99% Credible Interval')
        plt.plot(x, mean, c='w')
        return None

    def point_grid(model, coordinates=(-1, 1, .1), show_var=False):
        x_test, s = make_grid(coordinates)
        mean, var = model.posterior_predict(x_test)
        mean = atmost_1d(mean)
        var = atmost_1d(var)
        if show_var == False:
            plt.scatter(x_test[:, 0], x_test[:, 1], c=mean)
        else:
            plt.scatter(x_test[:, 0], x_test[:, 1], c=var)
        return None

    def contour(model, coordinates=(-1, 1, .1), show_var=False):
        x_test, s = make_grid(coordinates)
        mean, var = model.posterior_predict(x_test)
        mean = atmost_1d(mean)
        var = atmost_1d(var)
        if show_var == False:
            z = mean.T.reshape(s, s)
        else:
            z = np.sqrt(var).T.reshape(s, s)
        a, b = x_test.T.reshape(2, s, s)
        plt.contourf(a, b, z, 20, cmap='RdGy')
        plt.colorbar()
        contours = plt.contour(a, b, z, 5, colors='black')
        plt.clabel(contours, inline=True, fontsize=8)
        return None

    def plot_3d(model, coordinates=(-1, 1, .1), show_var=False, figsize=(20, 10)):
        x_test, s = make_grid(coordinates)
        mean, var = model.posterior_predict(x_test)
        mean = atmost_1d(mean)
        var = atmost_1d(var)
        if show_var == False:
            z = mean.T.reshape(s, s)
        else:
            z = np.sqrt(var).T.reshape(s, s)
        a, b = x_test.T.reshape(2, s, s)
        fig = plt.figure(figsize=figsize)

        ax = fig.add_subplot(221, projection="3d")
        ax.plot_surface(a, b, z, cmap="autumn_r", lw=0.5, rstride=1, cstride=1, alpha=0.5)
        ax.contour(a, b, z, 10, lw=3, colors="k", linestyles="solid")
        ax.view_init(30, -60)

        ax = fig.add_subplot(222, projection="3d")
        ax.plot_surface(a, b, z, cmap="autumn_r", lw=0.5, rstride=1, cstride=1, alpha=0.5)
        ax.contour(a, b, z, 10, lw=3, colors="k", linestyles="solid")
        ax.view_init(30, 60)

        ax = fig.add_subplot(223, projection="3d")
        ax.plot_surface(a, b, z, cmap="autumn_r", lw=0.5, rstride=1, cstride=1, alpha=0.5)
        ax.contour(a, b, z, 10, lw=3, colors="k", linestyles="solid")
        ax.view_init(30, 120)

        ax = fig.add_subplot(224, projection="3d")
        ax.plot_surface(a, b, z, cmap="autumn_r", lw=0.5, rstride=1, cstride=1, alpha=0.5)
        ax.contour(a, b, z, 10, lw=3, colors="k", linestyles="solid")
        ax.view_init(30, -120)
        return None

class classification:
    def plot_1dc(x, mean):
        x = atmost_1d(x)
        mean = atmost_1d(mean)
        plt.plot(x, mean, c='w')
        return None

    def contour(model, coordinates=(-1, 1, .1), show_var=False):
        x_test, s = make_grid(coordinates)
        if show_var == False:
            mean = model.posterior_predict(x_test)
            z = mean.T.reshape(s, s)
        else:
            mean, var = model.posterior_predict(x_test, True)
            z = np.mean(var, axis=1).T.reshape(s, s)
        a, b = x_test.T.reshape(2, s, s)
        plt.contourf(a, b, z, 20, cmap='RdGy')
        plt.colorbar()
        contours = plt.contour(a, b, z, 5, colors='black')
        plt.clabel(contours, inline=True, fontsize=8)
        return None
