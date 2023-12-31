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


def opt_1(start, data):
    yes = []
    no = []

    num_1 = start
    num_2 = start + 1

    before = data["Stress(MPa)"][num_1]
    after = data["Stress(MPa)"][num_2]
    #print("start ", start)
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
                #print("mark =", start)
                #print("stop =", num_1)
                break

    remove = count + start
    #print("end =", remove)
    return remove


def opt_lower(start, data):

    num_1 = start
    num_2 = start - 1
    #print("check")
    before = data["Stress(MPa)"][num_1]
    after = data["Stress(MPa)"][num_2]
    #print("start ", start)
    count = 0

    while True:
        if float(before) > float(after):
            count = count + 1
            num_1 = start - count
            num_2 = start - 1 - count

            before = data["Stress(MPa)"][num_1]
            after = data["Stress(MPa)"][num_2]

        else:
            #print("Done, count is =", count)
            break

    remove = start - count
    #print("end =", remove)
    return remove


def objective_2(data_entry, data):
    mark = -1
    while True:
        mark = mark + 1
        if data_entry[mark] == 0:
            break

    if set(data_entry) == {0, 1, 2, 3, 4, 5}:
        remove1 = mark
        while True:
            remove1 = remove1 + 1
            if data_entry[remove1] == 5:
                break

        remove1 = opt_1(remove1, data)
        #mark = opt_lower(mark, data)
        try:
            mark = opt_lower(mark, data)
        except Exception:
            mark = mark
        new_list = []
        count = -1
        while count < len(data_entry) - 1:
            count = count + 1
            if count < mark:
                new_list.append(0)
            elif count > remove1:
                new_list.append(0)
            else:
                new_list.append(1)
    else:
        remove1 = mark
        while True:
            remove1 = remove1 + 1
            if data_entry[remove1] == 5:
                break

        remove1 = opt_1(remove1, data)
        #mark = opt_lower(mark, data)
        try:
            mark = opt_lower(mark, data)
        except Exception:
            mark = mark
        new_list = []
        count = -1
        while count < len(data_entry) - 1:
            count = count + 1
            if count < mark:
                new_list.append(0)
            elif count > remove1:
                new_list.append(0)
            else:
                new_list.append(1)

    return new_list


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
    predict = objective_2(predict, data_s_2)

    data_s_2["Clusters"] = predict
    data_2 = data_s_2[data_s_2.Clusters != 0]
    data_2 = data_2.drop(['Clusters'], axis=1)

    plt.title("testID_0192")
    #sns.scatterplot(x="Strain", y="Stress(MPa)", data=data_s_2, hue=predict, palette='Set1')
    sns.scatterplot(x="Strain", y="Stress(MPa)", data=data_2, palette='Set1')
    plt.show()


clean_noise(screened_data('0192'))