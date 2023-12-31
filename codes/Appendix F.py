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
from sklearn.cluster import *

raw_data_folder = "/Users/admin/Library/CloudStorage/OneDrive-UniversityofCapeTown/final year project/01 screened data"


def screened_data(num):
    data = pd.read_csv(
        f"{raw_data_folder}/testID_{num}.csv")
    data = data[["Strain", "Stress(MPa)", "Time(sec)", "Force(kN)", "Jaw(mm)"]]
    return data


def opt_1(start, data):
    yes = []
    no = []

    num_1 = start
    num_2 = start + 1

    before = data["Stress(MPa)"][num_1]
    after = data["Stress(MPa)"][num_2]

    count = 0
    while True:
        if float(before) > float(after):
            yes.append(1)
        else:
            no.append(0)

        num_1 = num_1 + 1
        num_2 = num_2 + 1

        before = data["Stress(MPa)"][num_1]
        after = data["Stress(MPa)"][num_2]

        if (len(yes) + len(no)) == 6:
            if len(no) > 0:
                count = count + 1
                num_1 = start + count
                num_2 = start + count + 1

                before = data["Stress(MPa)"][num_1]
                after = data["Stress(MPa)"][num_2]

                yes = []
                no = []
            else:
                break

    remove = count + start
    return remove


def opt_lower(start, data):
    num_1 = start
    num_2 = start - 1
    after = data["Stress(MPa)"][num_1]
    before = data["Stress(MPa)"][num_2]
    count = 0

    while True:
        if float(before) > float(after):
            count = count + 1
            num_1 = start - count
            num_2 = start - 1 - count

            before = data["Stress(MPa)"][num_1]
            after = data["Stress(MPa)"][num_2]

        else:
            # print("Done, count is =", count)
            break

    remove = start - count
    # print("end =", remove)
    return remove


def objective_2(predict, data):
    mark = -1
    while True:
        mark = mark + 1
        if predict[mark] == 0:
            break

        mark = mark
    while True:
        mark = mark + 1
        if predict[mark] != 0:
            break

    median = (data["Strain"][len(data) - 1]) / 2

    mid = 0
    while True:
        mid = mid + 1
        if (abs(float(median - data['Strain'][mid]))) < 0.01:
            break

    num = predict[mid]
    upper = mid
    while True:
        upper = upper + 1
        if predict[upper] != num:
            break

    new_list = []
    remove = upper - 40

    remove = opt_1(remove, data)
    count = -1
    while count < len(predict) - 1:
        count = count + 1
        if count < mark:
            new_list.append(0)
        elif count > remove:
            new_list.append(0)
        else:
            new_list.append(1)
    return new_list


def clean_noise(data):
    model = DBSCAN(min_samples=20, eps=1)
    predict = model.fit_predict(data)

    predict = objective_2(predict, data)

    data["Clusters"] = predict
    data_2 = data[data.Clusters != 0]
    data_2 = data_2.drop(['Clusters'], axis=1)

    plt.title("testID_0128")
    sns.scatterplot(x="Strain", y="Stress(MPa)", data=data, hue=predict, palette='Set1')
    plt.show()
    sns.scatterplot(x="Strain", y="Stress(MPa)", data=data_2, palette='Set1')
    plt.show()


clean_noise(screened_data('0128'))