import paddle
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import gmm


def create_synthetic_data(num_gaussians, num_features, num_samples, means, vars):
    assert len(means[0]) == len(vars[0]) == num_features
    samples = []
    for g in range(num_gaussians):
        loc = paddle.to_tensor(data=means[g]).astype(dtype="float32")
        covariance_matrix = paddle.eye(num_rows=num_features).astype(
            dtype="float32"
        ) * paddle.to_tensor(data=vars[g]).astype(dtype="float32")
        dist = paddle.distribution.multivariate_normal.MultivariateNormal(
            loc=loc, covariance_matrix=covariance_matrix
        )
        for i in range(num_samples // num_gaussians):
            sample = dist.sample()
            samples.append(sample.unsqueeze(axis=0))
    samples = paddle.concat(samples, axis=0)
    return samples


def plot_data(data, y=None):
    if y is not None:
        for sample, target in zip(data, y):
            if target == 0:
                plt.scatter(*sample, color="blue")
            elif target == 1:
                plt.scatter(*sample, color="red")
            elif target == 2:
                plt.scatter(*sample, color="green")
    else:
        for sample in data:
            plt.scatter(*sample, color="black")
    plt.show(block=False)
    plt.pause(2)
    plt.close()


means = [[1, 4], [5, 5], [2, -1]]
vars = [[0.1, 0.1], [0.05, 0.4], [0.5, 0.2]]
data = create_synthetic_data(3, 2, 600, means, vars)
plot_data(data)
model = gmm.GaussianMixture(3, 2)
model.fit(data)
y = model.predict(data)
plot_data(data, y)
