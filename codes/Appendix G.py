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
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


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


def clusters(data):
    removed = []
    for i in data:
        if i < -0.05:
            removed.append(1)
        elif i <= 0.1:
            removed.append(2)
        elif i <= 0.13:
            removed.append(3)
        elif i < 0.2:
            removed.append(4)
        elif i < 0.35:
            removed.append(5)
        else:
            removed.append(0)

    return removed


def y_point(data_s, data_t):
    data_trim = []
    for i in data_t['Strain']:
        data_trim.append(i)

    removed = []
    for i in data_s['Strain']:
        if i in data_trim:
            removed.append(1)
        else:
            removed.append(0)

    return removed


def clean_noise(data_s_2):
    X_train = screened_data('0089')[["Strain", "Stress(MPa)"]]
    y_train = y_point(screened_data('0089'), trimmed_data('0089'))

    X_test = data_s_2[["Strain", "Stress(MPa)"]]
    y_test = y_point(screened_data("0095"), trimmed_data("0095"))

    model = PolynomialFeatures(degree=7)

    X_train = model.fit_transform(X_train)
    X_test = model.fit_transform(X_test)

    algo = LinearRegression()
    algo.fit(X_train, y_train)

    predict = algo.predict(X_test)
    predict = clusters(predict)

    data_s_2["Clusters"] = predict
    data_2 = data_s_2[data_s_2.Clusters != 0]
    data_2 = data_2.drop(['Clusters'], axis=1)

    plt.title("testID_0090")
    sns.scatterplot(x="Strain", y="Stress(MPa)", data=data_s_2, hue=predict, palette='Set1')
    plt.show()


clean_noise(screened_data('0090'))