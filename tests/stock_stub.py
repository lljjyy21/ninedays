import pandas as pd
import numpy as np


def get_stub():
    open_price = np.array([1002.97, 1011.34, 1006.73, 995.95, 994.62, 996.70, 995.78, 993.38, 980.35, 971.54,
                           970.70, 959.84, 958.49, 944.52, 966.07, 957.97, 961.35, 947.62, 948.95, 952.82])

    high_price = np.array([803.29, 805.75, 813.33, 816.00, 810.97, 811.07, 815.72, 816.49, 816.22, 819.20,
                           823.00, 824.26, 824.30, 811.35, 809.95, 799.00, 792.00, 785.28, 780.00, 770.50])

    low_price = np.array([789.62, 798.14, 802.44, 805.80, 805.11, 806.03, 805.10, 811.00, 804.50, 808.12,
                          812.00, 812.78, 811.94, 804.53, 798.05, 787.91, 773.53, 773.32, 766.97, 759.00])

    close_price = np.array([1010.07, 1002.97, 1011.34, 1006.73, 995.95, 994.62, 996.70, 995.78, 993.38, 980.35,
                            971.54, 970.70, 959.84, 958.49, 944.52, 966.07, 957.97, 961.35, 947.62, 948.95])

    volume = np.array([1735900, 1057400, 1214800, 976000, 765500, 1131600, 1459600, 1271900, 1263600, 2589100,
                       1768500, 1769700, 2103300, 1627300, 1894000, 1608300, 2018300, 1729800, 1682700, 1692600])

    date = pd.date_range('1/1/2015', periods=volume.shape[0], freq='D')

    data = pd.DataFrame({"Open": open_price, "High": high_price, "Low": low_price,
                         "Close": close_price, "Volume": volume, "Date": date})

    data = data.set_index("Date")

    return data
