from futsimulator.utils.plotting import get_plot


values = {"plot_1":[1,2,3,4,5,6,7],
          "plot_2":[5,5,5,5,5,5,5]}

path = 'plot.png'

get_plot(values, 'x_label_here', 'y_labe_herel', "title_here", path)