"""

"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from .filebase import load_csv_file


def conding(coms):
    """
    对公司名字进行编码
    例如传入的公司名字是com = ['中科院计算所','中金支付','中科院计算所','Google']
    则返回的应该是 [3, 2, 3, 1]
    :param com:公司名字列表
    :return: 公司编码列表
    """
    com_dict = {}
    y = []
    count = 0
    data_names = set(coms)

    for i in data_names:
        count += 1
        com_dict[i] = count
    for com in coms:
        y.append(com_dict[com])

    return y


def plot_tsne(file_path, **kwargs):
    """
    参考： https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
    将csv文件中的数据降维(使用TSNE)，并把图画出来
    :param file_path: csv文件
    :param kwargs:
    :       com_name:这个参数标记最后一列是否是公司名称，默认是True
    :       others:其他参数为sklearn中TSNE的所有参数
    """
    com_name = kwargs['com_name'] if 'com_name' in kwargs else True
    n_components = kwargs['n_components'] if 'n_components' in kwargs else 2
    perplexity = kwargs['perplexity'] if 'perplexity' in kwargs else 30
    early_exaggeration = kwargs['early_exaggeration'] if 'early_exaggeration' in kwargs else 12.0
    learning_rate = kwargs['learning_rate'] if 'learning_rate' in kwargs else 200.0
    n_iter = kwargs['n_iter'] if 'n_iter' in kwargs else 1000
    n_iter_without_progress = kwargs['n_iter_without_progress'] if 'n_iter_without_progress' in kwargs else 300
    min_grad_norm = kwargs['min_grad_norm'] if 'min_grad_norm' in kwargs else 1e-07
    metric = kwargs['metric'] if 'metric' in kwargs else 'euclidean'
    init = kwargs['init'] if 'init' in kwargs else 'random'
    verbose = kwargs['verbose'] if 'verbose' in kwargs else 0
    random_state = kwargs['random_state'] if 'random_state' in kwargs else None
    method = kwargs['method'] if 'method' in kwargs else 'barnes_hut'
    angle = kwargs['angle'] if 'angle' in kwargs else 0.5

    datas = np.array(load_csv_file(file_path))
    if com_name:
        X = datas[:, 0:-1].astype(np.int64)
        coms = datas[:, -1]
        y = conding(coms)

        model_tsne = TSNE(n_components=n_components, perplexity=perplexity, early_exaggeration = early_exaggeration,
                    learning_rate = learning_rate, n_iter = n_iter, n_iter_without_progress = n_iter_without_progress,
                    min_grad_norm = min_grad_norm, metric = metric, init = init, verbose = verbose,
                    random_state = random_state, method = method, angle = angle
                    )

        data_tsne = model_tsne.fit_transform(X)
        plt.scatter(data_tsne[:, 0], data_tsne[:, 1], c=y)
        plt.show()


def plot_pca(file_path, **kwargs):
    """
    参考： https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
    将csv文件中的数据降维(使用PCA)，并把图画出来
    :param file_path: csv文件
    :param kwargs:
    :       com_name:这个参数标记最后一列是否是公司名称，默认是True
    :       others: 其他参数为sklearn中PCA的所有参数,
                    为了画图，n_components的默认值由sklearn的None改为了2
    """
    com_name = kwargs['com_name'] if 'com_name' in kwargs else True
    n_components = kwargs['n_components'] if 'n_components' in kwargs else 2
    copy = kwargs['copy'] if 'copy' in kwargs else True
    whiten = kwargs['whiten'] if 'whiten' in kwargs else False
    svd_solver = kwargs['svd_solver'] if 'svd_solver' in kwargs else 'auto'
    tol = kwargs['tol'] if 'tol' in kwargs else 0.0
    iterated_power = kwargs['iterated_power'] if 'iterated_power' in kwargs else 'auto'
    random_state = kwargs['random_state'] if 'random_state' in kwargs else None

    datas = np.array(load_csv_file(file_path))
    if com_name:
        X = datas[:, 0:-1].astype(np.int64)
        coms = datas[:, -1]
        y = conding(coms)

        model_pca = PCA(n_components = n_components, copy = copy, whiten = whiten,
                        svd_solver = svd_solver, tol = tol, iterated_power = iterated_power,
                        random_state = random_state)
        data_pca = model_pca.fit_transform(X)

        print ("各个维度的方差比例为：\n" + str(model_pca.explained_variance_ratio_))
        plt.scatter(data_pca[:, 0], data_pca[:, 1], c=y)
        plt.show()

