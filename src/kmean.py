from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

# Tạo một dataset ví dụ
X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)

# Trực quan hóa dữ liệu ban đầu
plt.scatter(X[:, 0], X[:, 1], s=50)
plt.title("Original Data")
plt.show()

# Khởi tạo mô hình KMeans với số cụm K=4
def kmean_event(num, data):
    kmeans = KMeans(n_clusters=num)
    kmeans.fit(data)

    y_kmeans = kmeans.predict(X)
    centers = kmeans.cluster_centers_

    return y_kmeans, centers


