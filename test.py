import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import radviz


colors = [[0., 0., 1., 1.],
          [0., 0., 0., 0.],
          [1., 0., 0., 1.]]
df1 = pd.DataFrame({'A' : [1 , 0, 2], 'B' : [2, 0, 2], 'Name' : [0, 1, 1] })
print df1 
df2 = pd.DataFrame({'A' : [12, 0, 12], 'B' : [3, 0, 12], 'Name' : [0, 1, 1] })
plt.figure()
ax = radviz(df1, 'Name', color = colors)
ax1 = radviz(df2, 'Name', color = colors)
ax.legend().set_visible(False)
ax1.legend().set_visible(False)
plt.show()