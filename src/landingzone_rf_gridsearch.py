import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score, precision_score, accuracy_score
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.grid_search import GridSearchCV

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

def classifier_metrics(TP, FP, FN, TN):
    ''' calculates accuracy, true positive rate (tpr), false positive rate (fpr)
    positive predictive value (ppv), and f1 '''
    TP, FP, FN, TN = float(TP), float(FP), float(FN), float(TN) 
    P, N = TP + FN, TN + FP # number actual positive and negative
    acc = (TP + TN)/(P + N) # accuracy
    tpr = TP / P # true positive rate (recall, sensitivity)
    fpr = FP / N # false positive rate
    ppv = TP / (TP + FP) # positive predictive value, or precision
    f1 = 2 * TP / (2 * TP + FP + FN) # f1 score 
    return acc, tpr, fpr, ppv, f1

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

def grid_search_manual(max_depth_list, max_features_list, min_samples_per_split_list, \
                       min_samples_per_leaf_list, criterion_list, nt, nr, X, y):
    ''' Creates a random forest of with nt number of trees and parameters in each
    of the lists. Returns a list containing averages and standard deviations of
    the metrics calculated for nr iterations. '''
    columns = ['nt', 'md', 'mf', 'mss', 'msl', 'crit', 'acc_mn', 'tpr_mn', \
               'fpr_mn', 'ppv_mn', 'f1_mn', 'acc_std', 'tpr_std', 'fpr_std', \
               'ppv_std', 'f1_std']
    rn = 0
    rn_total = len(max_depth_list) * len(max_features_list) * len(min_samples_per_split_list) \
               * len(min_samples_per_leaf_list) * len(criterion_list)
    df_results = pd.DataFrame(columns = columns, index = range(rn_total))
    for md in max_depth_list:
        for mf in max_features_list:
            for mss in min_samples_per_split_list:
                for msl in min_samples_per_leaf_list:
                    for crit in criterion_list:
                        rfc = RandomForestClassifier(n_estimators = nt, \
                              criterion = crit, max_depth = md, \
                              min_samples_split = mss, min_samples_leaf = msl, \
                              max_features = mf, bootstrap = True, n_jobs = -1) 
                        params_run = [nt, md, mf, mss, msl, crit]
                        r = np.zeros((nr, 5))
                        for i in xrange(nr):
                            X_train, X_test, y_train, y_test = train_test_split(X, y)
                            rfc.fit(X_train, y_train)
                            y_pred = rfc.predict(X_test)
                            TP, FP, FN, TN = determine_confusion_matrix_counts(y_test, y_pred)
                            acc, tpr, fpr, ppv, f1 = classifier_metrics(TP, FP, FN, TN)
                            r[i, :] = [acc, tpr, fpr, ppv, f1]
                        acc_mn, acc_std = round(r[:, 0].mean(),4), round(r[:, 0].std(),4)
                        tpr_mn, tpr_std = round(r[:, 1].mean(),4), round(r[:, 1].std(),4)
                        fpr_mn, fpr_std = round(r[:, 2].mean(),4), round(r[:, 2].std(),4)
                        ppv_mn, ppv_std = round(r[:, 3].mean(),4), round(r[:, 3].std(),4)
                        f1_mn, f1_std = round(r[:, 4].mean(),4), round(r[:, 4].std(), 4)
                        means = [acc_mn, tpr_mn, fpr_mn, ppv_mn, f1_mn]
                        stddevs = [acc_std, tpr_std, fpr_std, ppv_std, f1_std]
                        run_results = np.asarray(params_run + means + stddevs)
                        df_results.iloc[rn] = np.resize(run_results,(1,len(run_results)))
                        rn += 1
                        print "Completed run {} of {}".format(rn, rn_total)
    df_results.sort_values('f1_mn', axis=0, ascending=False, inplace=True)
    return df_results


if __name__ == '__main__':
    # inputs 
    fname = 'Block_25thto26th_allresults.csv' #data
    nt = 30 # number of trees in random forest - for grid search will use 30
    # grid search parameters
    max_depth_list = [2, 4, 8, 10, 12, None] 
    max_features_list = [2, 4, 8] # 
    min_samples_per_split_list = [2, 4, 6] 
    min_samples_per_leaf_list = [1, 2, 4] 
    criterion_list = ["gini", "entropy"]
    nr = 30 # number of times to repeat analysis.  Because there are only about
    # 50 true positives in a group of over 1600 images, the train-test split
    # can severely affect the recall and precision of the result.  There aren't
    # enough TP to do a kfold properly.  So in this monte-carlo approach the train-test 
    # split is performed multiple times with random seeds and the precision, 
    # recall and f1 score are calculated and then the average is determined
   
    # calcuations
    df = load_data_into_dataframe(fname)
    X, y = extract_X_and_y_from_dataframe(df)
    df_grid_results = grid_search_manual(max_depth_list, max_features_list, \
                        min_samples_per_split_list, \
                        min_samples_per_leaf_list, criterion_list, nt, nr, X, y)
    df_grid_results.to_csv('grid_search_results_best_f1.csv')
    print "Parameters offering best f1 score:"
    print df_grid_results.head(10)
    df_grid_results.sort_values('ppv_mn', axis=0, ascending=False, inplace=True)
    df_grid_results.to_csv('grid_search_results_best_ppv.csv')
    print ""
    print "Parameters offering best ppv score:"
    print df_grid_results.head(10)

