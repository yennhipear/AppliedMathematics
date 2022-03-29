import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold

if __name__ == "__main__":
    reg = LinearRegression()
    df = pd.read_csv('wine.csv', sep = ';')

    x = df.drop("quality", axis = 1)        # Create a dataframe containing only data as a dependent variable
    y = df["quality"]                       # Create a dataframe containing "quality" data as a independent variable

    reg.fit(x, y)       # Create model

    #1.a
    print ("Sentence 1a: ")
    print(pd.DataFrame({"Name ":x.columns, "Coefficients ":reg.coef_}))     
    print("Normal error: ", reg.intercept_)
    print("\n")
   
    x = x.to_numpy()
    y = y.to_numpy()

    #1.b
    print ("Sentence 1b: ")
    kf = KFold(n_splits = 5)
    min_mse = 10000
    min_i = 0
    for i in range(x.shape[1]):
        mse = 0
        for train_idx, test_idx in kf.split(x):
            X_train_child = []
            X_test_child  = []
            X_train = []
            y_train = []
            X_test  = []
            y_test  = []

            for j in train_idx:          
                X_train.append(x[j])
                y_train.append(y[j])
            for j in test_idx:          
                X_test.append(x[j])
                y_test.append(y[j])
            
            X_train = np.array(X_train)
            y_train = np.array(y_train)
            X_test  = np.array(X_test)
            y_test  = np.array(y_test)

            for k in range(X_train.shape[0]):
                X_train_child.append(X_train[k][i])
            
            for k in range(X_test.shape[0]):
                X_test_child.append(X_test[k][i])
            
            X_train_child = np.array(X_train_child)
            X_test_child = np.array(X_test_child)

            X_train_child = np.reshape(X_train_child, (-1,1)) 
            X_test_child = np.reshape(X_test_child, (-1,1)) 

            reg.fit(X_train_child, y_train)
            y_pred = reg.predict(X_test_child)
           
            mse += mean_squared_error(y_test, y_pred)

        if (mse < min_mse):
            min_mse = mse
            min_i = i
    print ("The feature that gives the best results is in column: ", min_i)

    m = df.iloc[:, min_i]

    m = m.to_numpy()
    m = np.reshape(m, (-1,1)) 
    
    reg.fit(m, y)

    print("Coefficients: ", reg.coef_)
    print("Normal error: ", reg.intercept_)
    print("\n")
    
    #1.c
    print ("Sentence 1c: ")
    kf = KFold(n_splits = 5)
    min_mse = 10000
    X1_trainMin = []
    y1_trainMin = [] 

    X1_trainMin = np.array(X1_trainMin)
    y1_trainMin = np.array(y1_trainMin)

    for train_idx, test_idx in kf.split(x):
        mse = 0
        X1_train = []
        y1_train = []
        X1_test  = []
        y1_test  = []

        for j in train_idx:          
            X1_train.append(x[j])
            y1_train.append(y[j])
        for j in test_idx:          
            X1_test.append(x[j])
            y1_test.append(y[j])
        
        X1_train = np.array(X1_train)
        y1_train = np.array(y1_train)
        X1_test  = np.array(X1_test)
        y1_test  = np.array(y1_test) 

        reg.fit(X1_train, y1_train)
        y_pred = reg.predict(X1_test)
    
        mse = mean_squared_error(y1_test, y_pred)    
        if (mse < min_mse):
            min_mse = mse
            X1_trainMin = np.array(X1_train)
            y1_trainMin = np.array(y1_train)
    
    reg.fit(X1_trainMin, y1_trainMin)
    x1 = df.drop("quality", axis = 1)

    print(pd.DataFrame({"Name ":x1.columns, "Coefficients ":reg.coef_}))
    print("Normal error: ", reg.intercept_)

    print("\n")