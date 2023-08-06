
# coding: utf-8

# In[17]:


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
    QuadraticDiscriminantAnalysis()
]


# In[2]:


# Get data
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris["data"], iris["target"], test_size = 0.2)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, stratify=y_train,test_size = 0.3)
# Number of classes
m = len(np.unique(y_test))
# p(y) for train set
py = value_counts(y_train) / float(len(y_train))
print('Set sizes:', len(X_train), '(train),', len(X_val), '(val),', len(X_test), '(test)')


# In[3]:


# Hyper-parameters for LearningWithNoisyLabels() classifier
param_grid = {
    "cv_n_folds": [3,7],
    "clf": classifiers,
    "prune_method": ['prune_by_noise_rate', 'prune_by_class', 'both'],
    "prune_count_method": ['inverse_nm_dot_s', 'calibrate_confident_joint'],
    "converge_latent_estimates": [False, True],
}
# param_settings = list(ParameterGrid(param_grid))


# In[8]:


# Generate noise labels
noise_matrix = generate_noise_matrix_from_trace(m, trace = m / 1.5, py = py)
s = generate_noisy_labels(y_train, noise_matrix)


# In[15]:


from sklearn.metrics import accuracy_score

# Analyze results in parallel on all cores.
def _run_thread_job(param_setting):  
    try:
        # Seeding is important for fair comparison of param settings!
        clf = LearningWithNoisyLabels(**param_setting, seed = 0)
        clf.fit(X_train, s)        
        if hasattr(clf, 'score'):        
            score = clf.score(X_val,y_val)
        else:            
            score = accuracy_score(y_val, clf.predict(X_val))
        return (clf, score)

    except Exception as e:
        return None

def _parallel_param_opt(lst, threads=n_threads):
    pool = mp.Pool(threads)
    results = pool.map(_run_thread_job, lst)
    pool.close()
    pool.join()
    return results

def hyperparameter_optimization(
    X_train,
    y_train,
    clf = LearningWithNoisyLabels(),
    param_grid = {
        "cv_n_folds": [3, 5],
        "clf": classifiers,
        "prune_method": ['prune_by_noise_rate', 'prune_by_class', 'both'],
        "prune_count_method": ['inverse_nm_dot_s', 'calibrate_confident_joint'],
        "converge_latent_estimates": [False, True],
    },
    X_val = None, # validation data if it exists (if None, use crossval)
    y_val = None, # validation labels if they exist (if None, use crossval)
    num_threads = None, # Chooses max threads by default
    cv_folds = 3, # Only used if X_val, y_val are None
    verbose = True,
):
    '''Returns the clf trained with the hyperparameters that maximize accuracy
    on the (X_val, y_val) validation data (if specified), else the parameters
    that maximize cross fold validation score. Uses grid search to find the best
    hyper-parameters.
    
    Parameters
    ----------        
    X_train : np.array of shape (n, m)
        The training data.
        
    y_train : np.array of shape (n,) or (n, 1)
        The training labels. They can be noisy if you use clf = LearningWithNoisyLabels().
        
    clf : sklearn.classifier, default: LearningWithNoisyLabels()
        The classifier whose hyperparams you need to optimize with grid search.
        
    param_grid : dict (default is all parameters used by LearningWithNoisyLabels())
        The parameters to train with out on the validation set. Format
        is {'param1': ['list', 'of', 'options'], 'param2': ['l', 'o', 'o'], ...}
        
    X_val : np.array of shape (n0, m)
        The validation data to optimize paramters with. If you do not provide this,
        cross validation on the training set will be used. 
        
    y_val : np.array of shape (n0,) or (n0, 1)
        The validation labels to optimize paramters with. If you do not provide this,
        cross validation on the training set will be used. 
        
    num_threads : int (chooses max # of threads by default),
        The number of CPU threads to use.
        
    cv_folds : int (default 3)
        The number of cross-validation folds to use if no X_val, y_val is specified.
        
    verbose : bool
        Print out useful information when running.'''
    
    jobs = list(ParameterGrid(param_grid))
    
    if verbose:
        print("Running", len(jobs)//threads, "job(s) on", n_threads, "thread(s).")
    results = _parallel_param_opt(jobs, threads = n_threads)
    results = [result for result in results if result is not None]
    clfs, scores = list(zip(*results))
    best_idx = np.argmax(scores)
    best_clf, best_score = clfs[best_idx], scores[best_idx]
    if verbose:
        print("The classifier with the highest scoring parameters:")
        print(best_clf)
        print("Validation Accuracy:", round(best_score, 4))


# In[16]:


hyperparameter_optimization(X_train, s, X_val=X_val, y_val=y_val)

