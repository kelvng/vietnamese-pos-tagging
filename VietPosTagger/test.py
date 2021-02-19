from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn import datasets

iris = datasets.load_iris()
print(iris.target)
