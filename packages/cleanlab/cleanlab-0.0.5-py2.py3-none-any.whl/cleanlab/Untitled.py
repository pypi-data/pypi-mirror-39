
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
from cleanlab.classification import LearningWithNoisyLabels
from cleanlab.noise_generation import generate_noisy_labels
from cleanlab.noise_generation import generate_noise_matrix_from_trace
from cleanlab.util import value_counts
from cleanlab.util import print_noise_matrix
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
threads = mp.cpu_count()

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


# In[22]:


lol = LogisticRegression()


# In[34]:


import inspect
inspect.signature(np.abs)


# In[19]:


# Analyze results in parallel on all cores.
def thread_job(param_setting):  
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

def parallel_process(lst, threads=threads):
    pool = mp.Pool(threads)
    results = pool.map(thread_job, lst)
    pool.close()
    pool.join()
    return results

def hyperparameter_optimization(
    X_train,
    y_train,
    clf = LearningWithNoisyLabels(),
    clf_param_grid = {
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
    
    if X_val is None & y_val is not None | X_val is not None & y_val is None:
        raise ValueError('Only one of X_val and y_val are not None. Both must be specified.')
        
    
    jobs = list(ParameterGrid(clf_param_grid))
    
    if verbose:
        print("Running", len(jobs)//threads, "job(s) on", threads, "thread(s).")
    results = parallel_process(jobs)
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


# In[14]:


jobs = param_settings
if verbose:
    print("Running", len(jobs)//threads, "job(s) on", threads, "thread(s).")
results = parallel_process(jobs)
results = [result for result in results if result is not None]
clfs, scores = list(zip(*results))
best_idx = np.argmax(scores)
best_clf, best_score = clfs[best_idx], scores[best_idx]
if verbose:
    print(best_clf)
    print("Validation Accuracy:", round(best_score, 4))


# In[ ]:


# Hyper-parameter optimization via grid search for different amounts of noise.
num_traces = 100.
num_trials = 500
scores_no_opt = []
scores_opt = []
for trial in range(num_trials):
    print('Trial', trial)
    traces = np.arange(1.0 + (m - 1) / float(num_traces), m + 1e-5, (m - 1) / float(num_traces))
    scores_no_opt_per_trial = []
    scores_opt_per_trial = []
    # Iris Data: for trace in [1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3]
    try:
        for trace in traces:
        #     print("*"*80)

            # Generate noise labels
            noise_matrix = generate_noise_matrix_from_trace(m, trace, py = py)
            s = generate_noisy_labels(y_train, noise_matrix)

            scores = [] # store scores for the diff parameter options here
            trained_clfs = []
            list_of_params = list(ParameterGrid(param_grid))
            for params in list_of_params:
                clf = LearningWithNoisyLabels(**params)
                clf.fit(X_train, s)
                scores.append(clf.score(X_val,  y_val))
                trained_clfs.append(copy.deepcopy(clf))
            idx_best = np.argmax(scores)
            best_clf = trained_clfs[idx_best]
            rp = LearningWithNoisyLabels()
            rp.fit(X_train, s)
            score_no_opt = rp.score(X_test, y_test)
            scores_no_opt_per_trial.append(score_no_opt)
            score_opt = best_clf.score(X_test, y_test)
            scores_opt_per_trial.append(score_opt)
        scores_no_opt.append(scores_no_opt_per_trial)
        scores_opt.append(scores_opt_per_trial)
    except:
        continue

# Get average score across the trials
scores_no_opt = np.stack(scores_no_opt).mean(axis=0)
scores_opt = np.stack(scores_opt).mean(axis=0)


# In[49]:


plt.figure(figsize=(20,10))
plt.plot(traces, scores_no_opt, label = 'No', linewidth=3)
plt.plot(traces, scores_opt, label = 'yes', linewidth=3)
legend = plt.legend(title='Parameter optimization', fontsize=20)
plt.setp(legend.get_title(),fontsize=20)
plt.xticks([1.2,2,3], fontsize=25)
plt.yticks([0.5,0.75,1], fontsize=25)
plt.xlabel('Trace of noise matrix', fontsize=30)
plt.ylabel('Avg Accuracy (500 trials)', fontsize=30)
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

