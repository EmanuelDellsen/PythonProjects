from pylab import plot, show, savefig, xlim, figure, ylim, legend, boxplot, setp, axes, hist
import pylab
import scipy.stats as stats
import numpy as np

TCS = [[2.50, 4.33, 4.00, 6.00, 4.50, 6.40, 3.25, 6.40, 7.00, 6.33, 5.14, 6.00, 2.33, 5.50, 5.25, 4.25, 4.00, 3.50, 3.75, 4.00, 3.25, 3.50, 4.00, 4.50, 3.67, 4.83, 4.60, 4.00, 4.00, 5.25, 4.50, 6.67, 5.00, 3.33, 4.25, 2.00, 3.25, 2.50, 3.11, 6.75, 5.50, 3.75, 6.00, 4.00, 4.00, 4.20, 3.25, 4.00, 5.00, 5.00, 2.67, 2.83, 6.00, 4.20, 3.00, 2.60, 2.33, 4.00, 4.33, 6.33, 3.00, 3.00, 2.67, 2.14, 2.25, 1.60, 2.88, 3.00, 2.25, 3.00, 4.00, 3.00, 2.60, 1.82, 2.80, 1.86, 2.20, 4.00],
       [5.00, 6.00, 4.67, 5.25, 2.33, 4.00, 3.60, 1.86, 3.67, 4.83, 6.00, 5.75, 4.50, 5.00, 2.40, 2.80, 3.60, 5.00, 2.50, 3.00, 6.25, 4.25, 5.00, 5.33, 4.67, 3.00, 6.67, 2.50, 4.50, 4.00, 4.33, 2.75, 4.00, 4.00, 5.50, 3.67, 3.00, 6.00, 2.00, 3.00, 3.50, 3.00, 5.00, 2.50, 4.00, 3.17, 3.17, 3.00, 3.50, 2.50, 3.20, 2.80, 6.50, 2.44, 2.93, 4.00, 3.80, 3.25, 3.29, 3.33, 5.20, 5.25, 4.50, 4.00, 2.50, 2.60, 1.71, 2.44, 3.00, 3.00, 2.33, 3.00, 1.56, 1.58, 2.10, 1.73, 2.00, 2.33, 2.25, 3.00, 2.50, 1.80]]

TSS = [[2, 3, 3, 3, 6, 5, 4, 5, 2, 6, 7, 3, 6, 4, 4, 4, 2, 4, 4, 3, 4, 4, 5, 4, 3, 6, 5, 4, 3, 4, 4, 3, 4, 3, 4, 1, 4, 4, 9, 4, 4, 4, 3, 2, 3, 5, 8, 3, 3, 6, 3, 6, 3, 5, 1, 5, 6, 5, 3, 3, 7, 8, 3, 7, 4, 5, 8, 4, 4, 2, 5, 5, 5, 11, 5, 7, 5, 3],
       [4, 6, 3, 8, 3, 3, 5, 7, 3, 6, 2, 4, 6, 1, 5, 5, 5, 3, 4, 5, 4, 4, 3, 3, 3, 2, 3, 6, 4, 2, 3, 4, 4, 2, 4, 3, 4, 1, 6, 4, 2, 5, 2, 4, 2, 6, 6, 5, 6, 2, 10, 10, 4, 9, 15, 5, 5, 4, 7, 6, 5, 4, 2, 3, 2, 5, 7, 9, 3, 4, 3, 9, 9, 12, 10, 11, 5, 9, 4, 5, 12, 5]]

fig = figure()
ax = axes()

# hold(True)

bp = boxplot(TCS, positions=[1, 2], widths=0.6)

xlim(0, 3)
ylim(0, 8)
ax.set_xticklabels(['GM', 'US'])
ax.set_xticks([1, 2])

savefig('boxplotTCS.png')
show()

fig = figure()
ax = axes()

# hold(True)

bp = boxplot(TSS, positions=[1, 2], widths=0.6)

xlim(0, 3)
ylim(0, 16)
ax.set_xticklabels(['GM', 'US'])
ax.set_xticks([1, 2])

savefig('boxplotTSS.png')
show()


hist(TCS[0], rwidth=0.8)
savefig('histogramTCSGM.png')
show()

hist(TCS[1], rwidth=0.8)
savefig('histogramTCSUS.png')
show()

hist(TSS[0], rwidth=0.8)
savefig('histogramTSSGM.png')
show()

hist(TSS[1], rwidth=0.8)
savefig('histogramTSSUS.png')
show()

hist(np.concatenate((TSS[0], TSS[1])), rwidth=0.8)
savefig('histogramTSS.png')
show()

hist(np.concatenate((TCS[0], TCS[1])), rwidth=0.8)
savefig('histogramTCS.png')
show()

conc = np.concatenate((TCS[0], TCS[1]))
stats.probplot(conc, dist="norm", plot=pylab)
savefig('qqTCS.png')
show()

conc = np.concatenate((TSS[0], TSS[1]))
stats.probplot(conc, dist="norm", plot=pylab)
savefig('qqTSS.png')

show()
