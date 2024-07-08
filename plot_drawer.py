import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import requests
from io import StringIO
import numpy as np

class PlotDrawer:
    def __init__(self):
        self.plots_dir = "plots"
        self.distributions_dir = os.path.join(self.plots_dir, "parameter distributions")
        self.upper_triangle_dir = os.path.join(self.plots_dir, "columns comparings scatter")
        self.lower_triangle_dir = os.path.join(self.plots_dir, "columns comparings kde")
        for directory in [self.plots_dir, self.distributions_dir, self.upper_triangle_dir, self.lower_triangle_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def draw_plots(self):
        url = 'https://ai-process-sandy.s3.eu-west-1.amazonaws.com/purge/deviation.json'
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.read_json(StringIO(response.text))
        else:
            print(f'Error loading data: {response.status_code}')
            return []
        
        plot_paths = []
        # Building and saving parameter distributions
        deviation_columns = ['mean', 'max', 'min', 'floor_mean', 'floor_max', 'floor_min', 'ceiling_mean', 'ceiling_max', 'ceiling_min']
        for column in deviation_columns:
            plt.figure()
            sns.histplot(df[column], kde=True, bins=30)
            plt.title(f'Distribution of {column}')
            # Path to save the distribution plot
            distribution_plot_path = os.path.join(self.distributions_dir, f"{column}_distribution.png")
            plt.savefig(distribution_plot_path)
            plt.close()
            plot_paths.append(distribution_plot_path)
        
        # Building pair grids and saving each plot separately
        g = sns.PairGrid(df[deviation_columns])
        g.map_upper(sns.scatterplot)
        g.map_lower(sns.kdeplot, cmap="Blues_d", warn_singular=False)
        g.map_diag(sns.histplot, kde=True, bins=30)
        
        # Saving plots from the upper triangle
        for i, j in zip(*np.triu_indices_from(g.axes, 1)):
            plt.figure()
            sns.scatterplot(data=df, x=deviation_columns[j], y=deviation_columns[i])
            scatter_plot_path = os.path.join(self.upper_triangle_dir, f"{deviation_columns[j]}_vs_{deviation_columns[i]}_scatter.png")
            plt.savefig(scatter_plot_path)
            plt.close()
            plot_paths.append(scatter_plot_path)
        
        # Saving plots from the lower triangle
        for i, j in zip(*np.tril_indices_from(g.axes, -1)):
            plt.figure()
            sns.kdeplot(data=df, x=deviation_columns[j], y=deviation_columns[i], cmap="Blues_d", warn_singular=False)
            kde_plot_path = os.path.join(self.lower_triangle_dir, f"{deviation_columns[j]}_vs_{deviation_columns[i]}_kde.png")
            plt.savefig(kde_plot_path)
            plt.close()
            plot_paths.append(kde_plot_path)
        
        # Saving the overall plot with all plots at once
        pairgrid_plot_path = os.path.join(self.plots_dir, "pairgrid.png")
        g.savefig(pairgrid_plot_path)
        plt.close()
        plot_paths.append(pairgrid_plot_path)

        return plot_paths


plot_drawer = PlotDrawer()
plot_paths = plot_drawer.draw_plots()

for path in plot_paths:
    print(path)
