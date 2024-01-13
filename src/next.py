
import pandas as pd
from scipy import stats

# Data provided by the user
data = {
    "Commercial Power Energy Consumed": [10838, 11738, 11622, 10697],
    "SPAD Energy Consumed": [11022.3, 11622.77, 12017.52, 10763.4]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Perform a paired t-test
t_stat, p_value = stats.ttest_rel(df['Commercial Power Energy Consumed'], df['SPAD Energy Consumed'])

t_stat, p_value