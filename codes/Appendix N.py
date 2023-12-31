"""
This code was built by Katleho Mofokeng
Katleho's student number is MFKKATOO7
"""

import numpy as np
import pandas as pd
# from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns

raw_data_folder = "/Users/admin/Library/CloudStorage/OneDrive-UniversityofCapeTown/final year project/01 screened data"

trimmed_data_folder = "/Users/admin/Library/CloudStorage/OneDrive-UniversityofCapeTown/final year project/02 trimmed " \
                      "data"


def screened_data(num):
    data = pd.read_csv(
        f"{raw_data_folder}/testID_{num}.csv")
    data = data[["Strain", "Stress(MPa)", "Time(sec)", "Force(kN)", "Jaw(mm)"]]
    return data


def trimmed_data(num):
    data = pd.read_csv(f"{trimmed_data_folder}/testID_{num}.csv")
    data = data[["Strain", "Stress(MPa)", "Time(sec)", "Force(kN)", "Jaw(mm)"]]
    return data


def yield_method_2(data_entry):
    data = data_entry

    y1 = data['Stress(MPa)'][0]
    y2 = data['Stress(MPa)'][3]

    x1 = data['Strain'][0]
    x2 = data['Strain'][3]

    E_modulus = (y2 - y1) / (x2 - x1)

    data['strain offset'] = data['Strain'] + 0.01
    data['stress offset'] = data['Strain'] * E_modulus

    y1 = data['stress offset'][0]
    y2 = data['stress offset'][3]

    x1 = data['strain offset'][0]
    x2 = data['strain offset'][3]

    E_modulus = (y2 - y1) / (x2 - x1)
    y_intercept = y2 - (E_modulus * x2)

    print('E_modulus =', E_modulus)

    Eqn = E_modulus * data['Strain'] + y_intercept

    count = 0
    dis_list = []

    while count < len(data['Strain']) - 2:
        distance = abs(
            E_modulus * data['Strain'][count] - data['Stress(MPa)'][count] + y_intercept) / (
                           E_modulus ** 2 + 1)

        dis_list.append(distance)
        count = count + 1

    t = 1
    count = 0
    while t != min(dis_list):
        t = dis_list[count]
        count = count + 1

    yield_point = np.zeros(len(data['Strain']))
    yield_point[count - 1] = 1

    data["Yield point"] = yield_point

    plt.title("testID_0256")
    sns.scatterplot(x="Strain", y="Stress(MPa)", data=data, hue="Yield point")
    plt.plot(data['strain offset'][1:9], data['stress offset'][1:9], "r")
    plt.show()


yield_method_2(trimmed_data("0256"))