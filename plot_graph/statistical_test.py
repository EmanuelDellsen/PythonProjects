from scipy.stats import ks_2samp, mannwhitneyu
import numpy as np


def critValueRequation(sample1Size, sample2Size, cOfAlpha):
    print(sample1Size, sample2Size)
    result = cOfAlpha * \
        np.sqrt((sample1Size + sample2Size) / (sample1Size * sample2Size))
    print(result)
    return result


def sameDistribution(criticalValue, statistic):
    if(statistic < criticalValue):
        return True
    else:
        return False


TCS = [[2.50, 4.33, 4.00, 6.00, 4.50, 6.40, 3.25, 6.40, 7.00, 6.33, 5.14, 6.00, 2.33, 5.50, 5.25, 4.25, 4.00, 3.50, 3.75, 4.00, 3.25, 3.50, 4.00, 4.50, 3.67, 4.83, 4.60, 4.00, 4.00, 5.25, 4.50, 6.67, 5.00, 3.33, 4.25, 2.00, 3.25, 2.50, 3.11, 6.75, 5.50, 3.75, 6.00, 4.00, 4.00, 4.20, 3.25, 4.00, 5.00, 5.00, 2.67, 2.83, 6.00, 4.20, 3.00, 2.60, 2.33, 4.00, 4.33, 6.33, 3.00, 3.00, 2.67, 2.14, 2.25, 1.60, 2.88, 3.00, 2.25, 3.00, 4.00, 3.00, 2.60, 1.82, 2.80, 1.86, 2.20, 4.00],
       [5.00, 6.00, 4.67, 5.25, 2.33, 4.00, 3.60, 1.86, 3.67, 4.83, 6.00, 5.75, 4.50, 5.00, 2.40, 2.80, 3.60, 5.00, 2.50, 3.00, 6.25, 4.25, 5.00, 5.33, 4.67, 3.00, 6.67, 2.50, 4.50, 4.00, 4.33, 2.75, 4.00, 4.00, 5.50, 3.67, 3.00, 6.00, 2.00, 3.00, 3.50, 3.00, 5.00, 2.50, 4.00, 3.17, 3.17, 3.00, 3.50, 2.50, 3.20, 2.80, 6.50, 2.44, 2.93, 4.00, 3.80, 3.25, 3.29, 3.33, 5.20, 5.25, 4.50, 4.00, 2.50, 2.60, 1.71, 2.44, 3.00, 3.00, 2.33, 3.00, 1.56, 1.58, 2.10, 1.73, 2.00, 2.33, 2.25, 3.00, 2.50, 1.80]]

TSS = [[2, 3, 3, 3, 6, 5, 4, 5, 2, 6, 7, 3, 6, 4, 4, 4, 2, 4, 4, 3, 4, 4, 5, 4, 3, 6, 5, 4, 3, 4, 4, 3, 4, 3, 4, 1, 4, 4, 9, 4, 4, 4, 3, 2, 3, 5, 8, 3, 3, 6, 3, 6, 3, 5, 1, 5, 6, 5, 3, 3, 7, 8, 3, 7, 4, 5, 8, 4, 4, 2, 5, 5, 5, 11, 5, 7, 5, 3],
       [4, 6, 3, 8, 3, 3, 5, 7, 3, 6, 2, 4, 6, 1, 5, 5, 5, 3, 4, 5, 4, 4, 3, 3, 3, 2, 3, 6, 4, 2, 3, 4, 4, 2, 4, 3, 4, 1, 6, 4, 2, 5, 2, 4, 2, 6, 6, 5, 6, 2, 10, 10, 4, 9, 15, 5, 5, 4, 7, 6, 5, 4, 2, 3, 2, 5, 7, 9, 3, 4, 3, 9, 9, 12, 10, 11, 5, 9, 4, 5, 12, 5]]

alpha = 0.05
cOfAlpha = 1.36

testTCS = ks_2samp(TCS[0], TCS[1])
testTSS = ks_2samp(TSS[0], TSS[1])
print(testTCS, testTSS)

criticalValueTCS = critValueRequation(len(TCS[0])-1, len(TCS[1])-1, cOfAlpha)
criticalValueTSS = critValueRequation(len(TSS[0])-1, len(TSS[1])-1, cOfAlpha)
print(criticalValueTCS, criticalValueTSS)

print(sameDistribution(criticalValueTCS, testTCS.statistic))
print(sameDistribution(criticalValueTSS, testTSS.statistic))

print(mannwhitneyu(TCS[0], TCS[1], alternative='two-sided'))
print(mannwhitneyu(TSS[0], TSS[1], alternative='two-sided'))
