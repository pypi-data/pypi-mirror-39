
# coding: utf-8

# In[1]:


from hyperopt.model_selection import fit_model_with_grid_search


# In[2]:


from sklearn.datasets import load_iris
from sklearn.model_selection import ParameterGrid
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from confidentlearning.classification import LearningWithNoisyLabels
from confidentlearning.noise_generation import generate_noisy_labels
from confidentlearning.noise_generation import generate_noise_matrix_from_trace
from confidentlearning.util import value_counts
from confidentlearning.util import print_noise_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import copy
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import pyplot as plt
# Silence neural network SGD convergence warnings.
from sklearn.exceptions import ConvergenceWarning
import warnings
warnings.filterwarnings('ignore', category=ConvergenceWarning)

# For parallel processing
import multiprocessing as mp
n_threads = mp.cpu_count()

classifiers = [
    KNeighborsClassifier(n_neighbors=3),
    SVC(kernel="linear", C=0.025, probability=True, random_state=0),
    SVC(gamma=2, C=1, probability=True, random_state=0),
    LogisticRegression(random_state=0),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    MLPClassifier(alpha=1, random_state=0),
    AdaBoostClassifier(random_state=0),
    GaussianNB(),
    QuadraticDiscriminantAnalysis(),
#     GaussianProcessClassifier(kernel=RBF(), random_state=0)
]


# In[3]:


# Get data
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris["data"], iris["target"], test_size = 0.2)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, stratify=y_train,test_size = 0.3)
# Number of classes
m = len(np.unique(y_test))
# p(y) for train set
py = value_counts(y_train) / float(len(y_train))
print('Set sizes:', len(X_train), '(train),', len(X_val), '(val),', len(X_test), '(test)')


# In[4]:


# Hyper-parameters for LearningWithNoisyLabels() classifier
param_grid = {
    "cv_n_folds": [3,7],
    "clf": classifiers,
    "prune_method": ['prune_by_noise_rate', 'prune_by_class', 'both'],
    "prune_count_method": ['inverse_nm_dot_s', 'calibrate_confident_joint'],
    "converge_latent_estimates": [False, True],
}
# param_settings = list(ParameterGrid(param_grid))


# In[5]:


# Generate noise labels
noise_matrix = generate_noise_matrix_from_trace(m, trace = m / 1.5, py = py)
s = generate_noisy_labels(y_train, noise_matrix)
np.bincount(s)


# In[6]:


get_ipython().run_line_magic('time', 'fit_model_with_grid_search(LearningWithNoisyLabels(seed = 0), X_train, s, param_grid, X_val=X_val, y_val=y_val)')
print()
print()
get_ipython().run_line_magic('time', 'fit_model_with_grid_search(LearningWithNoisyLabels(seed = 0), X_train, s, param_grid)')

