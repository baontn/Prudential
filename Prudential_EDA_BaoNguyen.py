# -*- coding: utf-8 -*-
"""Pru1_descrip.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AmAfYu_HhVZNDD7KCSSV4agJni10jxSG
"""

!git clone https://github.com/baontn/Prudential.git

"""#Import and Functions"""

import pandas as pd
import numpy as np
import sklearn
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
!pip install researchpy
import researchpy
from keras.wrappers.scikit_learn import KerasClassifier
import plotly.express as px 
from numpy import where
from numpy import meshgrid
from numpy import arange
from numpy import hstack
from numpy import std
from numpy import mean

from datetime import datetime 
from scipy import stats
sns.set()

def cramer_v(dataframe, y_column, column_list=None,):
  if column_list is not None:
    for a in column_list:
      print(a)
      myfield1 = dataframe[a]
      myfield2 = y_column
      contTable = pd.crosstab(myfield1, myfield2)
      crosstab, results = researchpy.crosstab(myfield1, myfield2, test='chi-square')
      results
      print(results)
      df= (contTable.shape[0]-1)*(contTable.shape[1]-1)
      print("degree of freedom: ", df)
  else:
    for a in dataframe.columns:
      print(a)
      myfield1 = dataframe[a]
      myfield2 = y_column
      contTable = pd.crosstab(myfield1, myfield2)
      crosstab, results = researchpy.crosstab(myfield1, myfield2, test='chi-square')
      results
      print(results)
      df= (contTable.shape[0]-1)*(contTable.shape[1]-1)
      print("degree of freedom: ", df)

def na_remove(df):
  imputer = SimpleImputer(missing_values = np.NaN, strategy='most_frequent')
  impute = imputer.fit(df.iloc[:,:])
  df.iloc[:,:] = imputer.transform(df.iloc[:, :])
  return df

"""# Data Inspection and Cleansing"""

raw_data = pd.read_excel('Prudential/club_churn_train.xlsx')

raw_data.describe()

percent_missing = raw_data.isnull().sum() * 100 / len(raw_data)
missing_value_df = pd.DataFrame({'percent_missing': percent_missing})
display(missing_value_df)

df1 = raw_data.copy()

df1.describe()

# Dataframe that focuses on inforce members
df_i = df1.copy()
df_i = df_i.drop(df_i[df_i.MEMBERSHIP_STATUS=='CANCELLED'].index)

# Dataframe that focuses on cancelled members
df_c = df1.copy()
df_c = df_c.drop(df_c[df_c.MEMBERSHIP_STATUS=='INFORCE'].index)

df_c

df2 = raw_data.copy()
df2['START_DATE'] = list(map(lambda x: datetime.strptime(str(x),'%Y%m%d'), df2['START_DATE']))

df1

df_c['START_DATE'] = list(map(lambda x: datetime.strptime(str(x),'%Y%m%d'), df_c['START_DATE']))
df_c['END_DATE'] = list(map(lambda x: int(x), df_c['END_DATE']))
df_c['END_DATE'] = list(map(lambda x: datetime.strptime(str(x),'%Y%m%d'), df_c['END_DATE']))

df_c['DURATION'] = abs((df_c.END_DATE-df_c.START_DATE))

df_ca = df_c.copy()
df_cb = df_c.copy()

df_ca = df_ca.drop(df_ca[df_ca.MEMBERSHIP_PACKAGE=='TYPE-B'].index)
df_cb = df_cb.drop(df_cb[df_cb.MEMBERSHIP_PACKAGE=='TYPE-A'].index)

df_ia = df_i.copy()
df_ib = df_i.copy()

df_ia = df_ia.drop(df_ia[df_ia.MEMBERSHIP_PACKAGE=='TYPE-B'].index)
df_ib = df_ib.drop(df_ib[df_ib.MEMBERSHIP_PACKAGE=='TYPE-A'].index)

df1a = df1.copy()
df1b = df1.copy()

df1a = df1a.drop(df1a[df1a.MEMBERSHIP_PACKAGE=='TYPE-B'].index)
df1b = df1b.drop(df1b[df1b.MEMBERSHIP_PACKAGE=='TYPE-A'].index)

"""## Data and Correlation Analysis"""

df3 = raw_data.copy()
df3.drop(['ID', 'MEMBERSHIP_NUMBER', 'AGENT_CODE', 'START_DATE', 'END_DATE'], axis=1, inplace=True)
df3 = na_remove(df3)
df3

nominal_list = ['MEMBER_MARITAL_STATUS', 'MEMBER_GENDER', 'MEMBERSHIP_PACKAGE', 'PAYMENT_MODE']

cramer_v(df3, df3['MEMBERSHIP_STATUS'], nominal_list)

df1.drop(['START_DATE', 'END_DATE'], axis=1, inplace=True)

plt.figure(figsize=(10,10))
heatmap = sns.heatmap(df1.corr(method='kendall'), annot=True)
heatmap.set_title('Kendall Correlation Heatmap', fontdict={'fontsize':12}, pad=12)
plt.show()

"""## Looking at the years

#### This part I focus on the data about the years: how many members got in/out in a particular year. 
"""

yearlist = []
for i in df2.START_DATE:
  yearlist.append(i.year)

yearlist = np.array(yearlist)
years = np.unique(yearlist)

six = 0
sev = 0
eig = 0
nin = 0
ten = 0
ele = 0
twl = 0
thr = 0
for i in yearlist: 
  if i == 2006:
    six += 1
  elif i == 2007:
    sev += 1
  elif i == 2008:
    eig += 1
  elif i == 2009:
    nin += 1
  elif i == 2010:
    ten += 1
  elif i == 2011:
    ele += 1
  elif i == 2012:
    twl += 1
  elif i == 2013:
    thr += 1
chartp = np.array([six, sev, eig, nin, ten, ele, twl, thr])
mylabels = ["2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013"]
myexplode = [0.8, 0.05, 0.05, 0, 0, 0.1,0,0  ]

plt.pie(chartp, labels = mylabels, explode = myexplode,radius=1.2, autopct= lambda x: '{:5.1f}'.format(x), shadow = True)
plt.title("Pie chart of customers' start dates")
plt.show()

enddate = df2.END_DATE.dropna()
yearlist = []
for i in enddate: 
  i = int(i)
  yearlist.append(i)
yearlist = np.array(yearlist)

years = []
for i in yearlist:
  i = datetime.strptime(str(i),'%Y%m%d')
  years.append(i.year)
years = np.array(years)
list_years = np.unique(years)

sev = 0
eig = 0
nin = 0
ten = 0
ele = 0
twl = 0
thr = 0
for i in years: 
  if i == 2007:
    sev += 1
  elif i == 2008:
    eig += 1
  elif i == 2009:
    nin += 1
  elif i == 2010:
    ten += 1
  elif i == 2011:
    ele += 1
  elif i == 2012:
    twl += 1
  elif i == 2013:
    thr += 1
chartp = np.array([sev, eig, nin, ten, ele, twl, thr])
mylabels = [ "2007", "2008", "2009", "2010", "2011", "2012", "2013"]
myexplode = [0.8, 0.05, 0, 0, 0.1, 0.05, 0.05  ]

plt.pie(chartp, labels = mylabels, explode = myexplode,radius=1.2, autopct= lambda x: '{:5.1f}'.format(x), shadow = True)
plt.title("Pie chart of customers' end dates for cancelled customers")
plt.show()

years = np.array(years)
list_years = np.unique(years)

df_c

dur_a = df_ca.DURATION.dt.days
dur_b = df_cb.DURATION.dt.days

plt.figure
plt.hist([dur_a, dur_b], bins=10, label=['Type-A', 'Type-B'], stacked=True)
plt.legend(["Type-A", "Type-B"])
plt.title("Duration of cancelled members, group by type (days)")
plt.show()

df_c.isna().sum()

"""## Gender Percentage"""

#Gender percentage
f = 0
for x in df1.MEMBER_GENDER:
  if x =="F": 
    f+=1
print("Female percentage: ", f/len(df1.MEMBER_GENDER))

f = 0
for x in df_i.MEMBER_GENDER:
  if x =="F": 
    f+=1
print("Female percentage in inforce customers: ", f/len(df_i.MEMBER_GENDER))

f = 0
for x in df_c.MEMBER_GENDER:
  if x =="F": 
    f+=1
print("Female percentage in cancelled customers: ", f/len(df_c.MEMBER_GENDER))

"""## Annual Fee Distribution
### Annual Fees of all, cancelled, and inforce members in histograms
"""

def an_fee(df, title):

  af2 = []
  af = df.ANNUAL_FEES
  for a in af:
    if a<4e6:
      a=a
      af2.append(a)
  plt.hist(af2, bins=10)
  plt.xlim([0, 1.5e6])
  plt.title(f"Annual Fee of {title} Members")
  plt.show()

an_fee(df1, "general")
an_fee(df_c, "cancelled")
an_fee(df_i, "inforce")

"""## Membership term years distribution
### Membership term years of all, cancelled, and inforce members in histograms


"""

def member_term(df, titles):
  mt = df.MEMBERSHIP_TERM_YEARS
  plt.hist(mt, bins=4)
  plt.title(f"Membership term years {titles}")
  plt.show()

member_term(df1, "in general")
member_term(df_i, "inforce customer")
member_term(df_c, "cancelled customer")

"""
## Marital Status
### Marital Status Percentages of all, cancelled, and inforce members in pie charts"""

def marital_stat(dataframe, title):   
  m = 0
  s = 0
  w = 0
  d = 0
  ms = dataframe.MEMBER_MARITAL_STATUS
  for i in ms:
    if i == "M":
      m+=1
    elif i == "S":
      s+= 1
    elif i == "W":
      w +=1
    elif i =="D":
      d += 1
  chartp = [m,s,w,d]
  mylabels = ["M", "S", "W", "D" ]
  myexplode = [0.2,0.1,0.2, 0.4]
  plt.pie(chartp, labels = mylabels, explode = myexplode,radius=1.2, autopct= lambda x: '{:5.1f}'.format(x), shadow = True)
  plt.title(f"Pie chart of Marital Status  {title} customers")
  plt.show()

marital_stat(df1, "all recorded")
marital_stat(df_i, "inforce customer")
marital_stat(df_c, "cancelled customer")

"""## Annual Income
### Annual Income of all, cancelled, and inforce members in histograms
"""

def ann_in(df, title):
  ai2 = []
  ai = df.MEMBER_ANNUAL_INCOME
  for a in ai:
    if a<0.4e7:
      ai2.append(a)
  plt.hist(ai2, bins=15)
  plt.title(f"Annual Income of {title} Members")
  plt.show()

ann_in(df1, "general")
ann_in(df_i, "inforce")
ann_in(df_c, "cancelled")

"""## Member Occupations
### Member Occupation percentages of all, cancelled, and inforce members in pie charts
"""

def mem_occu(df, title): 
  moc = raw_data.MEMBER_OCCUPATION_CD.unique()

  on = 0
  tw = 0
  th = 0
  fo = 0
  fv = 0
  si = 0
  mo = df.MEMBER_OCCUPATION_CD
  for i in mo:
    if i == moc[0]:
      on+=1
    elif i == moc[1]:
      tw+= 1
    elif i == moc[6]:
      th +=1
    elif i == moc[3]:
      fo += 1
    elif i == moc[4]:
      fv += 1
    elif i == moc[2]:
      si += 1  
  
  chartp = [on,tw,th,fo, fv,si]
  mylabels = ["1", "2", "3", "4", "5", "6" ]
  myexplode = [0.1,0.1,0.4, 0.1, 0.3, 0.2]
  plt.pie(chartp, explode = myexplode,radius=1.2, autopct= lambda x: '{:5.2f}'.format(x),pctdistance=0.88, shadow = True)
  centre_circle = plt.Circle((0, 0), 0.70, fc='white')
  fig = plt.gcf()
  
# Adding Circle in Pie chart
  fig.gca().add_artist(centre_circle)
  plt.title(f"Occupation Status {title}")
  plt.legend(mylabels, loc = "lower left") 
  plt.show()

mem_occu(df1, "in general")
mem_occu(df_i, "of inforce customers")
mem_occu(df_c, "of cancelled customers")

"""## Member Age At Issue """

def mem_age(df, title):
  aa = df.MEMBER_AGE_AT_ISSUE
  plt.hist(aa, bins=20)
  plt.title(f"Member Age At Issue {title}")
  plt.show()

mem_age(df1, "in general")
mem_age(df_i, "inforce")
mem_age(df_c, "cancelled")

"""### Member Age at issue vs Marital status and Package"""

# Draw the box plot using pandas
boxplot = df1.boxplot(column=['MEMBER_AGE_AT_ISSUE'], by=['MEMBER_MARITAL_STATUS', 'MEMBERSHIP_PACKAGE'], figsize=(10, 10))
plt.title("Box plot of Age of issue of General customers with their marital status and membership package")

boxplot = df_c.boxplot(column=['MEMBER_AGE_AT_ISSUE'], by=['MEMBER_MARITAL_STATUS', 'MEMBERSHIP_PACKAGE'], figsize=(10, 10))
plt.title("Box plot of Age of issue of Cancelled customers with their marital status and membership package")

boxplot = df_i.boxplot(column=['MEMBER_AGE_AT_ISSUE'], by=['MEMBER_MARITAL_STATUS', 'MEMBERSHIP_PACKAGE'], figsize=(10, 10))
plt.title("Box plot of Age of issue of Remained customers with their marital status and membership package")

"""#####T Test 1
###### T Test to see if the difference between the Age of issue of Type A and Divorce cancelled customer with that of Type A and Divorce of all registered customers.
"""

age_a_d_c = df_ca.drop(df_ca[df_ca.MEMBER_MARITAL_STATUS!='W'].index).MEMBER_AGE_AT_ISSUE
age_a_d_g = df1a.drop(df1a[df1a.MEMBER_MARITAL_STATUS!='W'].index).MEMBER_AGE_AT_ISSUE
stats.ttest_ind(age_a_d_c, age_a_d_g)

"""#####T Test 2
###### T Test to see if the difference between the Age of issue of Type B and Divorce cancelled customer with that of Type B and Divorce of all registered customers.
"""

age_b_d_c = df_cb.drop(df_cb[df_cb.MEMBER_MARITAL_STATUS!='W'].index).MEMBER_AGE_AT_ISSUE
age_b_d_g = df1b.drop(df1b[df1b.MEMBER_MARITAL_STATUS!='W'].index).MEMBER_AGE_AT_ISSUE
stats.ttest_ind(age_b_d_c, age_b_d_g)

"""## Payment Mode
### Payment mode percentages of all, cancelled, and inforce members in pie charts
"""

def pamo(df, title):
  an = 0
  ml = 0
  sa = 0
  qt = 0
  sp = 0
  pm = df.PAYMENT_MODE
  for i in pm:
    if i == "ANNUAL":
      an+=1
    elif i == 'MONTHLY':
      ml+= 1
    elif i == 'SEMI-ANNUAL':
      sa+=1
    elif i == 'QUARTERLY':
      qt += 1
    elif i == 'SINGLE-PREMIUM':
      sp += 1 
  chartp = np.array([an, ml, sa, qt, sp])
  mylabels = ["Annual", "Monthly", "Semi-Annual", "Quarterly", "Single-Premium"]
  myexplode = [0.1, 0, 0.02, 0.1, 0 ]

  plt.pie(chartp, labels = mylabels, explode = myexplode,radius=1.2, autopct= lambda x: '{:5.1f}'.format(x), shadow = True, startangle=150)
  plt.title(f"Pie chart of {title} customers")
  plt.show()

pamo(df1, "in general")
pamo(df_i, "inforce")
pamo(df_c, "cancelled")

"""## Membership Packages
### Membership package percentages of all, cancelled, and inforce members in pie charts
"""

def mem_pac(df, title):
  t_a = 0
  t_b = 0
  mp = df.MEMBERSHIP_PACKAGE
  for i in mp:
    if i == "TYPE-A":
      t_a+=1
    elif i == 'TYPE-B':
      t_b+= 1
  chartp = np.array([t_a,t_b])
  mylabels = ["Type-A", "Type-B"]
  myexplode = [0.1, 0.1 ]

  plt.pie(chartp, labels = mylabels, explode = myexplode,radius=1.2, autopct= lambda x: '{:5.1f}'.format(x), shadow = True, startangle = 90)
  plt.title(f"Package of {title} customer")
  plt.show()

mem_pac(df1, "general")
mem_pac(df_i, "inforce")
mem_pac(df_c, "cancelled")

"""### Annual Fee vs Membership package """

boxplot = df1.boxplot(column=['ANNUAL_FEES'], by=['MEMBERSHIP_PACKAGE'], figsize=(10, 10))
boxplot.set_ylim([0, 0.4e6])
plt.title("Box plot of Annual fees of customers with their membership package")
boxplot = df_c.boxplot(column=['ANNUAL_FEES'], by=['MEMBERSHIP_PACKAGE'], figsize=(10, 10))
boxplot.set_ylim([0, 0.4e6])
plt.title("Box plot of Annual fees of Cancelled customers with their membership package")
boxplot = df_i.boxplot(column=['ANNUAL_FEES'], by=['MEMBERSHIP_PACKAGE'], figsize=(10, 10))
boxplot.set_ylim([0, 0.4e6])
plt.title("Box plot of Annual fees of Inforce customers with their membership package")

"""##### T-Test
###### T Test to see if the difference between the mean annual fee of Type B and inforce customer with that of Type B of all registered customers.
"""

an_fe_B_i = df_ib.ANNUAL_FEES
an_fe_B_g = df1b.ANNUAL_FEES
stats.ttest_ind(an_fe_B_i, an_fe_B_g)

"""### Member Age At issue vs Member Occupation and Package"""

# Draw the box plot using pandas
boxplot = df1.boxplot(column=['MEMBER_AGE_AT_ISSUE'], by=['MEMBER_OCCUPATION_CD', 'MEMBERSHIP_PACKAGE'], figsize=(15, 15))
plt.title("Box plot of Age of issue of General customers with their marital status and membership package")

boxplot = df_c.boxplot(column=['MEMBER_AGE_AT_ISSUE'], by=['MEMBER_OCCUPATION_CD', 'MEMBERSHIP_PACKAGE'], figsize=(15, 15))
plt.title("Box plot of Age of issue of Cancelled customers with their marital status and membership package")

boxplot = df_i.boxplot(column=['MEMBER_AGE_AT_ISSUE'], by=['MEMBER_OCCUPATION_CD', 'MEMBERSHIP_PACKAGE'], figsize=(15, 15))
plt.title("Box plot of Age of issue of Remained customers with their marital status and membership package")

"""### Membership term years vs Packages:"""

# Draw the box plot using pandas
boxplot = df1.boxplot(column=['MEMBERSHIP_TERM_YEARS'], by=['MEMBERSHIP_PACKAGE'], figsize=(10, 10))
plt.title("Box plot of Membership term years of customers with their membership package")
boxplot = df_c.boxplot(column=['MEMBERSHIP_TERM_YEARS'], by=['MEMBERSHIP_PACKAGE'], figsize=(10, 10))
plt.title("Box plot of Membership term years of cancelled customers with their membership package")
boxplot = df_i.boxplot(column=['MEMBERSHIP_TERM_YEARS'], by=['MEMBERSHIP_PACKAGE'], figsize=(10, 10))
plt.title("Box plot of Membership term years of inforce customers with their membership package")

"""##### T Test
###### T Test to see if the difference between the Membership term years of Type B and inforce customer with that of Type B of all registered customers.
"""

me_te_a_c = df_ca.MEMBERSHIP_TERM_YEARS
me_te_a_g = df1a.MEMBERSHIP_TERM_YEARS
stats.ttest_ind(me_te_a_c, me_te_a_g)

len(me_te_a_c)

"""### Membership term years vs Marital Status and Package:


"""

# Draw the box plot using pandas
boxplot = df1.boxplot(column=['MEMBERSHIP_TERM_YEARS'], by=['MEMBER_MARITAL_STATUS','MEMBERSHIP_PACKAGE'], figsize=(10, 10))
plt.title("Box plot of Age of issue of general customers with their marital status and membership package")
boxplot = df_c.boxplot(column=['MEMBERSHIP_TERM_YEARS'], by=['MEMBER_MARITAL_STATUS','MEMBERSHIP_PACKAGE'], figsize=(10, 10))
plt.title("Box plot of Age of issue of Cancelled customers with their marital status and membership package")
boxplot = df_i.boxplot(column=['MEMBERSHIP_TERM_YEARS'], by=['MEMBER_MARITAL_STATUS','MEMBERSHIP_PACKAGE'], figsize=(10, 10))
plt.title("Box plot of Age of issue of inforce customers with their marital status and membership package")

"""##### T Test 1
###### T Test to see if the difference between the Membership term years of Type A and Single cancelled customer with that of Type A and Single of all registered customers.
"""

me_te_a_s_c = df_ca.drop(df_ca[df_ca.MEMBER_MARITAL_STATUS!='S'].index).MEMBERSHIP_TERM_YEARS
me_te_a_s_g = df1a.drop(df1a[df1a.MEMBER_MARITAL_STATUS!='S'].index).MEMBERSHIP_TERM_YEARS
stats.ttest_ind(me_te_a_s_c, me_te_a_s_g)

len(me_te_a_s_c)

"""#####T Test 2
###### T Test to see if the difference between the Membership term years of Type A and Widowed cancelled customer with that of Type A and Widowed of all registered customers.
"""

me_te_a_w_c = df_ca.drop(df_ca[df_ca.MEMBER_MARITAL_STATUS!='W'].index).MEMBERSHIP_TERM_YEARS
me_te_a_w_g = df1a.drop(df1a[df1a.MEMBER_MARITAL_STATUS!='W'].index).MEMBERSHIP_TERM_YEARS
stats.ttest_ind(me_te_a_w_c, me_te_a_w_g)

len(me_te_a_w_c)

me_te_a_w_c = df_ca.drop(df_ca[df_ca.MEMBER_MARITAL_STATUS!='W'].index)
me_te_a_w_c

"""#####T Test 3
###### T Test to see if the difference between the Membership term years of Type A and Married cancelled customer with that of Type A and Married of all registered customers.
"""

me_te_a_m_c = df_ca.drop(df_ca[df_ca.MEMBER_MARITAL_STATUS!='M'].index).MEMBERSHIP_TERM_YEARS
me_te_a_m_g = df1a.drop(df1a[df1a.MEMBER_MARITAL_STATUS!='M'].index).MEMBERSHIP_TERM_YEARS
stats.ttest_ind(me_te_a_m_c, me_te_a_m_g)

len(df_c)/len(df1)

pop_b = round(len(df1)*0.655)
len(df_cb)/pop_b

pop_a = round(len(df1)*0.345)
len(df_ca)/pop_a



# Draw the box plot using pandas
boxplot = df_c.boxplot(column=['MEMBERSHIP_TERM_YEARS'], by=['MEMBER_MARITAL_STATUS'], figsize=(10, 10))
boxplot = df_i.boxplot(column=['MEMBERSHIP_TERM_YEARS'], by=['MEMBER_MARITAL_STATUS'], figsize=(10, 10))