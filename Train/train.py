import pickle
import numpy as np
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC



x_dic = pickle.load(open('x.p','rb'))
y_dic = pickle.load(open('y.p','rb'))

x = []
y = []
for i in range(len(x_dic)-90):
	x.append(x_dic[i].values())
	y.append(y_dic[i].values().index(1))
x = np.array(x)
y = np.array(y)

#write your code here
'''
clf = SVC()
clf.fit(x,y)

SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
gamma=0.0, kernel='rbf', max_iter=-1, probability=False, random_state=None,
shrinking=True, tol=0.001, verbose=False)
'''


#from sklearn.externals import joblib
#joblib.dump(clf, 'SVM.pkl')


# Split the dataset in two equal parts
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.8, random_state=0)

# Set the parameters by cross-validation
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

scores = ['precision']

for score in scores:
    print("# Tuning hyper-parameters for %s" % score)
    print

    clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5,scoring = score)
                       #scoring='%s_weighted' % 
					   
    clf.fit(X_train, y_train)

    print("Best parameters set found on development set:")
    print
    print(clf.best_params_)
    print
    print("Grid scores on development set:")
    print
    for params, mean_score, scores in clf.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r"
              % (mean_score, scores.std() * 2, params))
    print

    print("Detailed classification report:")
    print
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred))
    print


y_true, y_pred = y_test, clf.predict(X_test)
for i in range(len(y_true)):
    print y_dic[0].keys()[y_true[i]],'\t\t\t',y_dic[0].keys()[y_pred[i]]

from sklearn.externals import joblib
joblib.dump(clf, 'SVM.pkl')
