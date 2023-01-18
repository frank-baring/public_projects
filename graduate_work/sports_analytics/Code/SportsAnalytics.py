#New functions:
# Average -works same as BA.Average
# Stddev - works same as BA.Stddev

#changes
# Graph_Binned_stats_with_prediction - can now have multiple lines
# model_test - fixed issue with p-value

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.discrete.discrete_model as discrete_model
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import linprog


# In[ ]:

def LogisticRegTrain(X,Y,Const=True,weight = None,Missing = 'delete'):
    """Train a Logistic Regression Model

    Args:
        X: pandas DataFrame, or numpy ndarray
            independent variables, each column represents one variable
            X and Y has the same index
        Y: pandas DataFrame, or numpy ndarray
            dependent variable, one column
        Const: boolean, default True
            Indicator for the constant term (intercept) in the fit.
        weight: 1d numpy array,
            weight of each column
        Missing: 'delete','nearest','mean','median',constant number
            the method to handle the missing value

    Returns:
        A logistic regression model
    """
    # missing values
    dataSet = pd.concat([X,Y],axis=1)

    if Missing is 'delete':
        dataSet = dataSet.dropna()
    elif Missing is 'nearest':
        dataSet = dataSet.fillna(method='ffill')
        dataSet = dataSet.fillna(method='bfill')
    elif Missing is 'mean':
        values = dict(dataSet.mean())
        dataSet = dataSet.fillna(value=values)
    elif Missing is 'median':
        values = dict(dataSet.median())
        dataSet = dataSet.fillna(value=values)
    else:
        try:
            const = float(Missing)
        except:
            print("Error: Type of Missing. please enter one of 'delete','nearest','mean','median',constant number")
            return None
        dataSet = dataSet.fillna(const)
    X = dataSet[dataSet.columns.values[:-1]]
    Y = dataSet[dataSet.columns.values[-1]]

    # row weight
    if weight is not None:
        X = pd.DataFrame(data=X.values*weight,columns=X.columns.values,index=X.index)

    # model w/t or w/o constant
    if Const is True:
        X = sm.add_constant(X)
        columnsName=['const']+['x%s' % n for n in range(1,X.shape[1])]
    else:
        columnsName=['x%s' % n for n in range(1,X.shape[1])]

    # train the model
    model = discrete_model.Logit(Y, X)
    result = model.fit()


    try:
        mdlCoeff = pd.DataFrame(data=dict(result.params), index={'Coefficients'})
        mdlSE = pd.DataFrame(data=dict(result.bse), index={'Std error'})
        mdlPvalue = pd.DataFrame(data=dict(result.pvalues), index={'p-value'})

    except:
        mdlCoeff = pd.DataFrame(data=result.params, index=columnsName, columns={'Coefficients'}).T
        mdlSE = pd.DataFrame(data=result.bse, index=columnsName, columns={'Std error'}).T
        mdlPvalue = pd.DataFrame(data=result.pvalues, index=columnsName, columns={'p-value'}).T


    SummaryTable = pd.concat((mdlCoeff,mdlSE,mdlPvalue))
    SummaryTable.loc['Log-likelihood',SummaryTable.columns.values[0]] = result.llf
    SummaryTable.loc['Number valid obs',SummaryTable.columns.values[0]] = result.df_resid
    SummaryTable.loc['Total obs',SummaryTable.columns.values[0]] = result.nobs

    pd.set_option('display.float_format', lambda x: '%.4f' % x)
    SummaryTable = SummaryTable.fillna('')

    try:
        SummaryTable.index.name = Y.name
    except:
        pass

    print(SummaryTable)
    result.SummaryTable = SummaryTable
    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    return result


# In[ ]:


def LogisticRegPredict(model,X):
    """Make prediction based on the trained logistic regression model
    make sure input X is of the same format as training X data for the model

    Args:
        model: statsmodels.discrete.discrete_model.BinaryResultsWrapper
            a logistic regression model
        X: pandas DataFrame, or numpy ndarray
            independent variables, each column represents one variable

    Returns:
        Array of predictions
    """
    if 'const' in model.SummaryTable.columns.values:
        print('adding constant')
        X = sm.add_constant(X, has_constant='add')
    print(X)
    prediction = model.predict(X)

    data = pd.DataFrame(data=X,columns=list(model.SummaryTable.columns.values))
    if 'const' in model.SummaryTable.columns.values:
        data = data.drop(['const'],axis=1)
    data['prediction'] = prediction
    #data.style.format({'prediction':"{:.2%}"})

    result = data
    return(result)


# In[ ]:
def LinearRegTrain(X,Y,Const=True,weight = None,Missing = 'delete'):
    """Train a Linear Regression Model

    Args:
        X: pandas DataFrame, or numpy ndarray
            independent variables, each column represents one variable
            X and Y has the same index
        Y: pandas DataFrame, or numpy ndarray
            dependent variable, one column
        Const: boolean, default True
            Indicator for the constant term (intercept) in the fit.
        weight: 1d numpy array,
            weight of each column
        Missing: 'delete','nearest','mean','median',constant number
            the method to handle the missing value

    Returns:
        A linear regression model
    """
    # missing values
    dataSet = pd.concat([X,Y],axis=1)

    if Missing is 'delete':
        dataSet = dataSet.dropna()
    elif Missing is 'nearest':
        dataSet = dataSet.fillna(method='ffill')
        dataSet = dataSet.fillna(method='bfill')
    elif Missing is 'mean':
        values = dict(dataSet.mean())
        dataSet = dataSet.fillna(value=values)
    elif Missing is 'median':
        values = dict(dataSet.median())
        dataSet = dataSet.fillna(value=values)
    else:
        try:
            const = float(Missing)
        except:
            print("Error: Type of Missing. please enter one of 'delete','nearest','mean','median',constant number")
            return None
        dataSet = dataSet.fillna(const)
    X = dataSet[dataSet.columns.values[:-1]]
    Y = dataSet[dataSet.columns.values[-1]]

    # row weight
  #  if weight is not None:
  #      X = pd.DataFrame(data=X.values*weight,columns=X.columns.values,index=X.index)

    # model w/t or w/o constant
    if Const is True:
        X = sm.add_constant(X)
        columnsName=['const']+['x%s' % n for n in range(1,X.shape[1])]
    else:
        columnsName=['x%s' % n for n in range(1,X.shape[1])]

    # train the model
    if weight is not None:
        model = sm.WLS(Y, X, weights=weight)
        result = model.fit()
    if weight is None:
        model = sm.OLS(Y, X)
        result = model.fit()

    try:
        mdlCoeff = pd.DataFrame(data=dict(result.params), index={'Coefficients'})
        mdlSE = pd.DataFrame(data=dict(result.bse), index={'Std error'})
        mdlPvalue = pd.DataFrame(data=dict(result.pvalues), index={'p-value'})

    except:
        mdlCoeff = pd.DataFrame(data=result.params, index=columnsName, columns={'Coefficients'}).T
        mdlSE = pd.DataFrame(data=result.bse, index=columnsName, columns={'Std error'}).T
        mdlPvalue = pd.DataFrame(data=result.pvalues, index=columnsName, columns={'p-value'}).T


    SummaryTable = pd.concat((mdlCoeff,mdlSE,mdlPvalue))
    SummaryTable.loc['Log-likelihood',SummaryTable.columns.values[0]] = result.llf
    SummaryTable.loc['Number valid obs',SummaryTable.columns.values[0]] = result.df_resid
    SummaryTable.loc['Total obs',SummaryTable.columns.values[0]] = result.nobs

    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    #SummaryTable.style.format("{:.2f}")
    SummaryTable = SummaryTable.fillna('')

    try:
        SummaryTable.index.name = Y.name
    except:
        pass

    print(SummaryTable)
    result.SummaryTable = SummaryTable

    return result

def LinearRegPredict(model,X):
    """Make prediction based on the trained linear regression model
    make sure input X is of the same format as training X data for the model

    Args:
        model: statsmodels linear regression model
        X: pandas DataFrame, or numpy ndarray
            independent variables, each column represents one variable

    Returns:
        Array of predictions
    """
    if 'const' in model.SummaryTable.columns.values:
        X = sm.add_constant(X)

    prediction = model.predict(X)

    data = pd.DataFrame(data=X,columns=list(model.SummaryTable.columns.values))
    if 'const' in model.SummaryTable.columns.values:
        data = data.drop(['const'],axis=1)
    data['prediction'] = prediction
    #data.style.format({'prediction':"{:.2%}"})

    result = data
    return(result)


# todo here
def Binned_stats(buckets,col1,col2,includeSE=None,SEMultiplier=None,includeSD=None,SD=None):
    """Print the table of binned stats

    Args:
        buckets: list of float
            a list of buckets boundaries
        col1: pandas DataFrame, or numpy ndarray
            reference column
        col2: pandas DataFrame, or numpy ndarray
            data value column
        includeSE: boolean
            indicator of whether to include standard error in the stats
        SEMultiplier: float
            Standard error multiplier
        includeSD: boolean
            indicator of whether to include standard deviation in the stats
        SD: float
            Standard deviation array

    Returns:
        table of binned stats
    """
    dataDic = {}

    idxLable = []
    count = []
    avg1 = []
    avg2 = []
    stderr2 = []
    stdd2 = []
    for i in range(len(buckets)-1):
        idxLable.append('[%s,%s)' % (buckets[i],buckets[i+1]))
        count.append(col1[(col1>=buckets[i])&(col1<buckets[i+1])].count())
        avg1.append(col1[(col1>=buckets[i])&(col1<buckets[i+1])].mean())
        avg2.append(col2[(col1>=buckets[i])&(col1<buckets[i+1])].mean())
        stderr2.append(col2[(col1>=buckets[i])&(col1<buckets[i+1])].sem()*2)

    idxLable[-1] = ('[%s,%s]' % (buckets[i],buckets[i+1]))

    dataDic['Bins'] = idxLable
    dataDic['Count'] = count
    dataDic['Avg '+col1.name] = avg1
    dataDic['Avg '+col2.name] = avg2
    dataDic['Stderr '+col2.name] = stderr2

    orderList = ['Bins','Count','Avg '+col1.name,'Avg '+col2.name,'Stderr '+col2.name]
    SummaryTable = pd.DataFrame(data=dataDic)[orderList]
    print(SummaryTable)
    return SummaryTable



# In[ ]:


def Graph_Binned_stats(binned_stats):
    """Draw the graph

    Args:
        binned_stats: pandas DataFrame
            output summary table of function Binned_stats()
    """
    colName = list(binned_stats.columns.values)
    fig = plt.figure(figsize=(10,8))
    plt.errorbar(binned_stats[colName[2]], binned_stats[colName[3]], yerr=binned_stats[colName[4]],fmt=".",capsize=5)
    plt.show()
    return fig


#Tom added linestyle as option and allowing multiple lines to be plotted
def Graph_Binned_stats_with_prediction(binned_stats,lineX,lineY,linestyle,lineX2 = None,lineY2 = None,linestyle2 = None):
    """Draw the graph

    Args:
        binned_stats: pandas DataFrame
            output summary table of function Binned_stats()
        line_x: x input to graph for predictions
        line_y: y output of prediciton
        linestyle: style of line
        line_x2: second x input to graph for predictions
        line_y2: second y output of prediciton
        linestyle2: second style of line
    """
    #fig = Graph_Binned_stats(binned_stats)
    colName = list(binned_stats.columns.values)
    fig = plt.figure(figsize=(10,8))
    plt.errorbar(binned_stats[colName[2]], binned_stats[colName[3]], yerr=binned_stats[colName[4]],fmt=".",capsize=5)

    if lineX2 != None:
        plt.plot(lineX,lineY,linestyle,lineX2,lineY2,linestyle2)

    else:
        plt.plot(lineX,lineY,linestyle)

    plt.xlabel('distance')
    plt.ylabel('make')

    return fig


# In[ ]:


def Bayes_normal(mean,stdev,Nob,sample_mean,sample_stdev):
    """Print the table of binned stats

    Args:
        mean: float
            mean of the population
        stdev: float
            standard deviation of population
        Nob: int
            number of observations
        sample_mean: float
            mean of the sample
        sample_stdev: float
            standard deviation of sample

    Returns:
        table of binned stats
    """

    post_m = (mean/stdev**2 + Nob*sample_mean/sample_stdev**2) / (1/stdev**2 + Nob/sample_stdev**2)
    post_sd = np.sqrt( 1 / (1/stdev**2 + Nob/sample_stdev**2) )

    return post_m,post_sd


# In[ ]:


def RMSE(errorValues = None,PredictionValue = None, Truth = None):
    """Calculate the RMSE of each model

    Args:
        errorValues: pandas Dataframe
            matrix of errors from different model, each column represents 1 series of error
        PredictionValue: pandas Dataframe
            matrix of predictions from different model, each column represents 1 series of prediction
        Truth: pandas Dataframe
            array of truth, 1 column

    Returns:
        table of RMSE
    """
    if errorValues is not None:
        if PredictionValue is None and Truth is None:
            rmseArray = np.sqrt(np.mean(errorValues**2,axis=0))
        else:
            print('Error: only define errorValues, or only define PredictionValue and Truth')
            return None
    else:
        if PredictionValue is not None and Truth is not None:
            rmseArray = np.sqrt(np.mean((PredictionValue.transpose()-Truth)**2))
        else:
            print('Error: only define errorValues, or only define PredictionValue and Truth')
            return None

    return rmseArray


# In[ ]:


def model_test(errorValues = None, PredictionValue = None, Truth = None):
    """calculate the RMSE of each model and p-value matrix and result of pairwise comparison among models

    Args:
        PredictionValue: pandas Dataframe
            matrix of predictions from different model, each column represents 1 series of prediction
        Truth: pandas Dataframe
            array of truth, 1 column

    Returns:
        table of RMSE and p-value matrix of each model
    """
    # rmseArray = np.sqrt(np.mean((PredictionValue.transpose()-Truth)**2,axis=1))
    # print(rmseArray)

    # calculate the squared error, and use it in the following sentences


    # blabla
    if errorValues is not None:
        if PredictionValue is None and Truth is None:
            rmseArray = np.sqrt(np.mean(errorValues**2,axis=0))
            sqErr = errorValues.values**2
            names = list(errorValues.columns.values)
        else:
            print('Error: only define errorValues, or only define PredictionValue and Truth')
            return None
    else:
        if PredictionValue is not None and Truth is not None:
            rmseArray = np.sqrt(np.mean((PredictionValue.values-Truth.values)**2,axis=0))
            sqErr = (PredictionValue.values-Truth.values)**2
            names = list(PredictionValue.columns.values)
        else:
            print('Error: only define errorValues, or only define PredictionValue and Truth')
            return None

    pvalueMatrix = np.empty(shape = (sqErr.shape[1],sqErr.shape[1]))
    pvalueMatrix[:] = np.nan

    for eachCol in range(sqErr.shape[1]):
        for eachCol2 in range(eachCol+1,sqErr.shape[1]):
            tmp_t,tmp_p = stats.ttest_rel(sqErr[:,eachCol], sqErr[:,eachCol2])
            pvalueMatrix[eachCol,eachCol2] = 1 - tmp_p/2 #TOM BLISS ADDITION
            pvalueMatrix[eachCol2,eachCol] = tmp_p/2 #TOM BLISS ADDITION

    SummaryTable = pd.DataFrame(data=pd.DataFrame(np.concatenate([rmseArray[:,None],pvalueMatrix],axis=1).T))
    SummaryTable.columns = names
    SummaryTable.index = ["RMSE"]+names
    print(SummaryTable)
    SummaryTable = SummaryTable.fillna('')
    return SummaryTable


#Tom's Additions:
def Average(Array1, row_weight):
    """calculate a weighted mean

    Args:
        Array1: Array of numbers.
        row_weight: weight of each number in average

    Returns:
        A weighted mean
    """

    return np.average(Array1, weights = row_weight)


def Stddev(Array1, row_weight):
    """calculate a weighted standard deviation

    Args:
        Array1: Array of numbers.
        row_weight: weight of each number in average

    Returns:
        A weighted standard deviaiton
    """

    return np.sqrt(np.cov(Array1, aweights=row_weight))
