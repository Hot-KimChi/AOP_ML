import numpy as np
import pandas as pd

dates = pd.date_range('20220518', periods=6)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('1234'))
print(df)