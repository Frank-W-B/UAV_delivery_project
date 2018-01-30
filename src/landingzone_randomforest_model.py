import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score, precision_score, accuracy_score
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

def load_data_into_dataframe(fname):
    ''' loads csv file into dataframe '''
    df = pd.read_csv(fname)
    return df

def extract_X_and_y_from_dataframe(df):
    ''' extracts the features and target from the dataframe '''
    y = df['lz'] # landing zone, 0 or 1 (1 is True)
    X = df.copy()
    del X['address']
    del X['img_num']
    del X['lz']
    return X, y

def train_model(X_train, y_train, ntrees, mspl):
    ''' trains a random forest classifier with ntrees estimators and mspl
        mininum samples per leaf '''
    forest = RandomForestClassifier(n_estimators = ntrees, n_jobs = -1, \
                                     min_samples_leaf = mspl)
    forest.fit(X_train, y_train)
    return forest 

def evaluate_model(forest, X_test, y_test): # could also define threshold here
    ''' evaluates the model with the test data ''' 
    y_pred = forest.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    return y_pred, accuracy, recall, precision

def determine_confusion_matrix_counts(y_test, y_pred):
    ''' determines and labels the true positives (TP), false positives (FP),
        false negatives (FN), and true negatives (TN).  Predicting a landing
        zone correctly is a TP, a non-landing zone correctly is a TN, a non-
        landing zone as a landing zone is a FP, and a landing zone as a non-
        landing zone is a FN.  1 is a landing zone, 0 is not a landing zone '''
    nr = len(y_test) # number of rows
    TP, FP, FN, TN = 0, 0, 0, 0
    for i in xrange(nr):
        y_true = y_test.iloc[i]
        y_predict = y_pred[i]
        if y_predict == 1:
            if y_true == 1:
                TP += 1
            else:
                FP += 1
        else: # y_predict is 0
            if y_true == 0:
                TN += 1
            else:
                FN += 1
    return TP, FP, FN, TN
            
def display_feature_importances(forest, X):
    ''' determines what features are most important '''
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_], \
                  axis = 0)
    indices = np.argsort(importances)[::-1]
    print("Feature ranking:")
    for f in range(X.shape[1]):
        print("%d. feature %d (%f)  %s" % (f + 1, indices[f], \
             importances[indices[f]], X.columns[indices[f]]))

def display_model_metrics(ntrees, mspl, accuracy, recall, precision, y_test, y_pred):
    ''' display model metrics '''
    num_lz_in_ytest = y_test.sum() # number of landing zones in test 
    num_in_test = len(y_test) # number of rows in test
    print "\nNumber of trees {}, minimum samples per leaf {}".format(ntrees, mspl)
    print "\nThere were {} rows in the test set.".format(num_in_test)
    print "There were {} landing zones in y_test.".format(num_lz_in_ytest)
    print "\nSklearn metrics"
    print "Accuracy {},  recall {},  precision {}".format(round(accuracy, 3), \
          round(recall, 3), round(precision, 3))
    print "\nConfusion matrix:"
    print(confusion_matrix(y_test, y_pred))
    TP, FP, FN, TN = determine_confusion_matrix_counts(y_test, y_pred)
    print "\n         Correctly identified landing zone (True positive): ", TP
    print "    Incorrectly indicated as landing zone (False positive): ", FP
    print "  Incorrectly classified l.z. as non-l.z. (False negative): ", FN
    print "  Correctly classifed non-l.z. as non-l.z. (True negative): ", TN
    print "\nClassification report:" 
    y_names = ['no landing zone, 0', 'landing zone, 1']
    print(classification_report(y_test, y_pred, target_names = y_names))

if __name__ == '__main__':
    # inputs 
    fname = 'Block_25thto26th_allresults.csv'
    ntrees = 1000 # number of trees in random forest
    mspl = 1 # minimum number of samples per leaf
    
    # calcuations
    df = load_data_into_dataframe(fname)
    X, y = extract_X_and_y_from_dataframe(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    forest = train_model(X_train, y_train, ntrees, mspl)
    y_pred, accuracy, recall, precision = evaluate_model(forest, X_test, y_test)
    
    # outputs 
    display_model_metrics(ntrees, mspl, accuracy, recall, precision, y_test, y_pred)
    display_feature_importances(forest, X) 
