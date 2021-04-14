from prmp_lib.prmp_gui.plot_canvas import *
from prmp_lib.prmp_gui import *



rt = Tk(themeIndex=37, tm=0)




pl = PRMP_PlotCanvas(rt.cont, place=dict(relx=.05, rely=.05, relw=.9, relh=.9))


def load():
    freq = list(range(2045, 7046, 500))
    hdb = [9.63, 11.37, 12.77, 13.98, 15.39, 15.91, 17.08, 17.72, 18.42, 19.17, 20.0]
    # hdb = [-1*a for a in hdb]

    # freq, hdb = hdb, freq
    
    # print(hdb)
    # print(freq)

    pl.doPlotting(xticks=freq, ys=hdb, grid=dict(lw=2), chart='plot')
    # pl.draw()








pl.after(100, load)




# load()





rt.start()







