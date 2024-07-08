import cProfile
import pstats
from plot_drawer import PlotDrawer

def profile_draw_plots():
    plot_drawer = PlotDrawer()
    plot_paths = plot_drawer.draw_plots()
    for path in plot_paths:
        print(path)

# Запуск профилирования
cProfile.run('profile_draw_plots()', 'profile_stats')

# Создание отчета
p = pstats.Stats('profile_stats')
p.sort_stats('cumulative').print_stats(10)  # Вывод 10 самых "тяжелых" функций
