import pandas as pd
import numpy as np
import seaborn as sns
from os import path
import matplotlib.pyplot as plt

def dataManipulation(cid):
    filePath = r'./dataset/'+str(cid)+'.csv'
    if not path.exists(filePath): # 判断cid是否正确
        print('please input correct CID')
        return 
    df_test = pd.read_csv(filePath)
    #df_test.drop(columns=['CID','CATEGORY','MANUFACTURER_NAME','PRODUCT_NAME'],inplace=True)
    df_test.drop(columns=['CID','MANUFACTURER_NAME','PRODUCT_NAME'],inplace=True)
    df_test['Grand Total'] = df_test.mean(numeric_only=True, axis=1)
    df_test.ffill(inplace=True)
    nan_percent =100*(df_test.isnull().sum()/len(df_test))>0.4
    nan_value = nan_percent[nan_percent.values==True].index
    df_test.drop(columns= nan_value,inplace=True)
    df_test['COLLECTION_DATE'] = pd.to_datetime(df_test['COLLECTION_DATE']) # transform date into proper type
    return df_test

def strategy_one(df,colName):
    dataFrame =df.copy(deep=True) # get a copy of origin dataframe, so the following editting won't change origin
    newColName = 'strategy1'+colName #define: column name = strategy+platform 
    dataFrame[newColName] = dataFrame['Grand Total']
    return dataFrame,newColName

def strategy_two(df,colName):
    dataFrame =df.copy(deep=True)
    newColName = 'strategy2'+colName
    dataFrame[newColName] = dataFrame['Grand Total'].rolling(5,min_periods=1).mean()
    return dataFrame,newColName


def strategy_three(df,colName):
    # get platform name,dataframe,
    # each day extreme price difference
    # return expected dataframe, new column name
    dataFrame =df.copy(deep=True)
    newColName = 'strategy3'+colName
    dataFrame[newColName] = dataFrame[colName]+dataFrame['Amazon']-dataFrame['Target']
    return dataFrame,newColName


def strategy_four(df,colName,costPercentage =0.8):
    # get platform name,dataframe,cost percentage in total price
    # current avg product price *0.8 = cost, using cost as model baseline  
    # return expected dataframe, new column name
    dataFrame =df.copy(deep=True)
    newColName = 'strategy4'+colName
    
    def baseToMean(curPrice, Grand):
        if curPrice*costPercentage >Grand:
            return curPrice*costPercentage
        else:
            return Grand
    dataFrame[newColName] = dataFrame[[colName,'Grand Total']].apply(lambda x:baseToMean(x[colName],x['Grand Total']),axis =1)

    return dataFrame,newColName



def strategy_five(pDf,colName):
    # input: pDf:product dataframe must include category Rate    
    # output:
    #        new product price vary with category index
    productDf = pDf.copy(deep=True)
    productDf['RATE'] = productDf['RATE'].str.rstrip('%').astype('float') / 100.0
    productDf['RATE'].fillna(0.0,inplace =True)
    #dfCategory = pd.merge(productDf,cateDf,how='left',left_on=['COLLECTION_DATE','CATEGORY'],right_on=['COLLECTION_DATE','CATEGORY'])
    newColName = 'strategy5'+colName
    productDf[newColName] = productDf[colName]*(1+productDf['RATE'])
    return productDf,newColName    


def demandRevenue(dataframe, colName):
    df =  dataframe.copy(deep=True)
    # df['Demand'+colName]=100-0.7*df[colName]+0.5*(df["Grand Total"]-df[colName])
    df['Demand'+colName]=df.apply(lambda x: max(0,(100-0.7*x[colName]+0.5*(x["Grand Total"]-x[colName]))),axis =1) 
    df['Revenue'+colName]=df['Demand'+colName]*df[colName]
    return df



def Visualization(x ,y1,y2):
    # x：日期 datatype: datetime
    # y1：不同策略revenue差值 series
    # y2: 该策略的价格 series
    # 最佳策略的strategy price 以及 culminative revenue   
    
    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax1 = fig.add_subplot(111)
    ax1.fill_between(x, np.cumsum(y1), color="skyblue", alpha=0.2, label="Cumulative Difference")
    ax1.plot(x, np.cumsum(y1), color="Slateblue", alpha=0.6)
    ax1.legend(loc="upper left")
    ax1.set_ylabel('Revenue Contribution')
    ax1.set_xlabel('Date')
    ax2 = ax1.twinx()  # this is the important function
    ax2.plot(x, y2, color='darkorange',alpha=0.7, label="Price")
    ax2.legend(loc="upper center")
    ax2.set_ylabel('Price')
    plt.xticks(pd.date_range('2020-06','2022-12',freq='4m'))
    plt.savefig('./output/BestStrategy.png')
    plt.show()



def visualizeRevenue(origin,revenueS1,revenueS2,revenueS3,revenueS4,revenueS5):
    # origin: origin revenue 
    # revenueS1..3 : Total revenue for strategy 1 to 3
    # datatype: Dataframe
    label=['original', 'strategy1','strategy2','strategy3','strategy4','strategy5']
    revenue_value=[origin.sum(),revenueS1.sum(),revenueS2.sum(),revenueS3.sum(),revenueS4.sum(),revenueS5.sum()]
    fig = plt.figure(figsize=(6, 4), dpi=100)
    plt.bar(label,revenue_value, color='skyblue')
    plt.axhline(origin.sum(),color='black',alpha=0.7,linestyle='--')
    plt.title("Total revenue of different strategies")
    plt.savefig('./output/rvnCp.png')
    plt.show()

 
def heatmap(dataframe):
    # input dataframe
    # output  correlation heatmap among all platform
    Platlist = ['Kohls','Target','Macys','Walmart','Amazon','AlbeeBaby','JCPenney','Overstock','Wayfair']
    dfchart = dataframe.copy(deep=True)
    dfchart = dfchart[dfchart.columns & Platlist]
    dftemp=dfchart.copy(deep=True)

    for i in range(1,dftemp.shape[0]):
        dftemp.iloc[i,:]=(100*(dfchart.iloc[(i),:]-dfchart.iloc[i-1,:])/dfchart.iloc[i,:])
        i=i+1

    df_correlation=dftemp.corr()
    ax=plt.figure(figsize=(6, 4), dpi=100)
    ax = sns.heatmap(df_correlation,annot=True)
    fig_heat = ax.get_figure()
    fig_heat.savefig('./output/heatMap.png')
    fig_heat.show()

def workflow(PlatName,pid,cstPercnt):
    #PlatName = input('plz input platform name')
 
    df_test = dataManipulation(pid)
    df1 = df_test.copy(deep=True)
    if PlatName not in df1.columns:
        print('please input the existed platform')
        return 0
    df2=demandRevenue(df1,PlatName)
    df2, c3name= strategy_three(df2,PlatName)
    df3= demandRevenue(df2,c3name)
    df3, c2name= strategy_two(df3,PlatName)
    df4 =demandRevenue(df3,c2name)
    df4, c1name= strategy_one(df4,PlatName)
    df5 =demandRevenue(df4,c1name)
    df5, c4name= strategy_four(df5,PlatName,cstPercnt)
    df6 =demandRevenue(df5,c4name)

    #data prepare for strategy five
    dfcate = pd.read_csv(r'./dataset/CATEGORY CHANGE.csv')
    dfcate['COLLECTION_DATE']=pd.to_datetime(dfcate['COLLECTION_DATE'])
    dfCategory = pd.merge(df6,dfcate,how='left',left_on=['COLLECTION_DATE','CATEGORY'],right_on=['COLLECTION_DATE','CATEGORY'])
   
    df6, c5name= strategy_five(dfCategory,PlatName)
    df7 =demandRevenue(df6,c5name)
    #df5.head()

    ori_revenue = df7['Revenue'+PlatName].sum()
    revenue1=(df7['Revenue'+c1name]).sum()-ori_revenue
    revenue2=(df7['Revenue'+c2name]).sum()-ori_revenue
    revenue3=(df7['Revenue'+c3name]).sum()-ori_revenue
    revenue4=(df7['Revenue'+c4name]).sum()-ori_revenue
    revenue5=(df7['Revenue'+c5name]).sum()-ori_revenue
    revenueCompare = {'strategy1':round(revenue1,2),
                        'strategy2':round(revenue2,2),
                        'strategy3':round(revenue3,2),
                        'strategy4':round(revenue4,2),
                        'strategy5':round(revenue5,2)}
    max_key = str(max(revenueCompare,key=revenueCompare.get))
    max_value = str(max(revenueCompare.values()))
    max_strategy =max_key+': '+max_value
    
    print(revenueCompare)
    print(max_strategy)
    Visualization(pd.to_datetime(df7['COLLECTION_DATE']),df7['Revenue'+ max_key+PlatName]-df7['Revenue'+PlatName],df7[max_key+PlatName])
    visualizeRevenue(df7['Revenue'+PlatName],df7['Revenuestrategy1'+PlatName],df7['Revenuestrategy2'+PlatName],df7['Revenuestrategy3'+PlatName],df7['Revenuestrategy4'+PlatName],df7['Revenuestrategy5'+PlatName])
    heatmap(df7)

    return max_key,max_value

def StrategyDic(key):
    Sdictionary={
        'strategy1': 'To use different strategy based on Q3 and Q1/2/4.' ,
        'strategy2': 'To change the price based on the 5-days rolling average price',
        'strategy3': 'To maintain the same change rate of its most relevant website.' ,
        'strategy4': 'To change the price based on 2rd strategy and knock out when p <cost.',
        'strategy5': 'To maintain the same volatility of the corresponding Category Index.'
    }
    return  Sdictionary[key]

def StrategyName(key):
    Sdictionary={
        'Strategy1': 'Time Segment Strategy' ,
        'Strategy2': 'Average Strategy',
        'Strategy3': 'Single Competitor Strategy' ,
        'Strategy4': 'Cost & Average Strategy',
        'Strategy5': 'Index Strategy'
    }
    return  Sdictionary[key]