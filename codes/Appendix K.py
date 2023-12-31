"""
This code was built by Katleho Mofokeng
Katleho's student number is MFKKATOO7
"""

import pandas as pd
# from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns

trimmed_data_folder = "/Users/admin/Library/CloudStorage/OneDrive-UniversityofCapeTown/final year project/02 trimmed " \
                      "data"


def trimmed_data(num):
    data = pd.read_csv(f"{trimmed_data_folder}/testID_{num}.csv")
    data = data[["Strain", "Stress(MPa)", "Time(sec)", "Force(kN)", "Jaw(mm)"]]
    return data


def elastic_modulus(data):
    y1 = data['Stress(MPa)'][0]
    y2 = data['Stress(MPa)'][3]

    x1 = data['Strain'][0]
    x2 = data['Strain'][3]

    E_modulus = (y2 - y1) / (x2 - x1)

    print('Elastic modulus =', E_modulus, "MPa")

    plt.title("testID_0256")
    sns.scatterplot(x="Strain", y="Stress(MPa)", data=data, palette='Set1')
    plt.show()


elastic_modulus(trimmed_data('0256'))