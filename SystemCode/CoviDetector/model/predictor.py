###########################################################################################
# (1D) compare the recommendations obtained using the above association rules with the recommendations obtained
# using a decision tree classifier (or any other supervised prediction model type you choose) to build one decision model per item.
# This is also a familiarity exercise for using scikitlearn prediction models and decisiontrees
############################################################################################
import os
import numpy as np
import pandas as pd
from random import sample
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


# make and test recommendations from a set of classifiers (one per item) for the test users
def classifierhits_holdout_lift(classifiers,testset,allitems,topN=1):
    hits = randhits = tests = 0
    allpreds = list()
    for username in testset.index:
        user = testset.loc[[username]] # extract user as dataframe
        for testitem in allitems:
            if (user.loc[username,testitem] == 1): # its been bought by user hence can use as a holdback (test) item
                tests += 1
                probs = dict()
                unseenitems = list()
                user.loc[username,testitem] = 0 # blank out value
                # make a prediction (exec the corresponding tree) for every item not yet seen/bought by user
                for unseenitem in allitems:
                    if (user.loc[username,unseenitem] == 0):  # its a valid unseen item
                        unseenitems.append(unseenitem)
                        inputvars = list(user.columns)
                        inputvars.remove(unseenitem)
                        pred = classifiers[unseenitem].predict_proba(user[inputvars])
                        probs[unseenitem] = pred[0][1] # get prob for class = True (the second element), Note: can check order returned with clf.classes_
                user.loc[username,testitem] = 1 # restore holdback value
                recs = sorted(probs.items(), key=lambda kv: kv[1], reverse=True) # sort unseen items by reverse probability
                numrecs = min(len(recs),topN)
                for item, conf in recs[0:numrecs]:
                    if (item == testitem):
                        hits += 1; break
                if (testitem in sample(unseenitems,numrecs)): randhits += 1 # make random recommedations
                allpreds.append((testitem,recs[0:numrecs])) # record the recommendations made
    lift = hits/randhits if randhits > 0 else np.nan
    print("tests=",tests,"rulehits=",hits,"randhits=",randhits,"lift=", lift)




####################################################
# (step1) load and preprocess the data
# preproceesing includes one-hot encoding the categorical variables

# path = 'D:/ISS/EBAC/EBAC-certs/BAP-Process/RecommenderSystems/Workshops/ZZworkshops'
path = './data'
os.chdir(path)
users = pd.read_csv('corona_tested_20201115.csv')
del users['cardid']

# swap the value T/F in all of the grocery variables to the grocery item name (this aids the onehot coding below)
# if we dont do this then the one-hot coded column names are assigned the values "T" and "F"
groceryitems = ['fruitveg', 'freshmeat', 'dairy', 'cannedveg', 'cannedmeat', 'frozenmeal', 'beer', 'wine', 'softdrink',
                'fish', 'confectionery']
for col in groceryitems:
    users[col] = np.where(users[col] == 'T', col, 'none')
users['homeown'] = np.where(users['homeown'] == 'YES', 'homeown', 'none')  # also do same for homeown variable

# onehot encode all of the categorical variables
# after one-hot coding a variable, we delete the original (unencoded) variable
catvars = set(users.columns) - set(('value', 'income', 'age'));
catvars
for v in catvars:
    onehot = pd.get_dummies(users[v])
    if 'none' in list(onehot.columns): onehot.drop('none', inplace=True, axis=1)
    users.drop(v, inplace=True, axis=1)
    users = users.join(onehot)

# view the preprocessed dataset (do a visual check for correctness)
users.columns
users

####################################################
# (step2) Build and test a decision tree for one item, with no pruning

# create train and test split
testsize = int(len(users) * 0.2);
testsize  # set the size of the test set (20%)
testnames = set(sample(list(users.index), testsize));
len(testnames)
trainnames = set(users.index) - testnames;
len(trainnames)
train = users.loc[trainnames,];
train.shape
test = users.loc[testnames];
test.shape

# build the decision tree
target = 'fruitveg'  # select the target item, any item will do
inputvars = list(set(users.columns) - set([target]))
tclf = tree.DecisionTreeClassifier()
tclf.fit(train[inputvars], train[target])

# view the tree method1
text_representation = tree.export_text(tclf, feature_names=inputvars)
print(text_representation)

# view the tree method2
plt.rcParams['figure.dpi'] = 200  # adjust to get the plot resolution you want
_ = tree.plot_tree(tclf, feature_names=inputvars, class_names=target, filled=True)

# test the tree
preds = tclf.predict(test[inputvars])
print(classification_report(test[target], preds))
print(confusion_matrix(test[target],
                       preds))  # rows = actual, cols = preds, eg precision for class 0 = (0,0)/((0,0)+(1,0))

# try some tree pruning to improve prediction accuracy (experiment with different pruning amounts to try to get best accuracy)
tclf = tree.DecisionTreeClassifier(min_samples_leaf=20)
tclf.fit(train[inputvars], train[target])
preds = tclf.predict(test[inputvars]);
preds
predsa = tclf.predict_proba(test[inputvars]);
predsa

# has the accuracy improved? if not then try a different amount of pruning or type of pruning
print(classification_report(test[target], preds))
print(confusion_matrix(test[target], preds))

####################################################
# (step3) build a tree for each grocery item and use these trees to make and test recommendations

# build the trees (one per grocery item) and store in a dictionary
trees = dict()
for target in groceryitems:
    inputvars = list(users.columns)
    inputvars.remove(target)
    clf = tree.DecisionTreeClassifier(min_samples_leaf=20)
    clf.fit(train[inputvars], train[target])
    print(target, 'tree size=', clf.tree_.node_count)  # size of the tree
    trees[target] = clf

# do the test for a range of topN values
# are the results better than the association rule results?
# (note: try running the below a few times, the lifts may vary due to the randomness of the random recommendations)

for n in range(1, 5):
    _ = classifierhits_holdout_lift(trees, test, groceryitems, topN=n)

####################################################