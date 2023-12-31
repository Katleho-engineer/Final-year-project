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
from sklearn.mixture import GaussianMixture


raw_data_folder = "/Users/admin/Library/CloudStorage/OneDrive-UniversityofCapeTown/final year project/01 screened data"


def screened_data(num):
    data = pd.read_csv(
        f"{raw_data_folder}/testID_{num}.csv")
    data = data[["Strain", "Stress(MPa)", "Time(sec)", "Force(kN)", "Jaw(mm)"]]
    return data


model_KMeans = KMeans(n_clusters=4, random_state=15)
model_MiniBatchKMeans = MiniBatchKMeans(n_clusters=8, random_state=15)
model_DBSCAN = DBSCAN(min_samples=20, eps=1)
model_AffinityPropagation = AffinityPropagation(preference=-100, random_state=15)
model_Agglomerative = AgglomerativeClustering(n_clusters=7)
model_MeanShift = MeanShift(bandwidth=17)
model_Spectral = SpectralClustering(n_clusters=2, random_state=15)
model_Birch = Birch(branching_factor=100, n_clusters=None, threshold=10.5)
model_Optics = OPTICS(min_samples=25)  #
model_GaussianMixture = GaussianMixture(n_components=10, random_state=15)


def compare(model, data_entry):
    data = data_entry
    remove = model.fit_predict(data_entry)
    data["test"] = remove

    plt.figure(figsize=(8, 8))
    plt.title("Pair plot of test 0090")
    sns.pairplot(data_entry, hue='test', palette='Set1')
    plt.show()


compare(model_GaussianMixture, screened_data('0089'))