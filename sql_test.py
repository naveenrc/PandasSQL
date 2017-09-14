import matplotlib.pyplot as plt
from pandasql import *
import pandas as pd
from _datetime import date


cu = pd.read_csv('customer.csv')
pr = pd.read_csv('product.csv')
pu = pd.read_csv('purchase.csv')

pu.columns = ['PurchaseID', 'ProductID', 'CustomerID', 'PurchasePrice', 'PurchaseDate']
pu['PurchaseDate'] = pd.to_datetime(pu['PurchaseDate'])
pysqldf = lambda q: sqldf(q, globals())

q = """
Select FirstName, LastName, ProductName, PurchasePrice from pu 
left join cu on cu.CustomerID==pu.CustomerID left join pr on pu.ProductID==pr.ProductID
where PurchaseDate between '2016-10-01' and '2016-10-31';
"""
q1 = """
Select DISTINCT cu.CustomerID, FirstName, LastName from pu 
left join cu on cu.CustomerID==pu.CustomerID
where PurchaseDate not BETWEEN '2016-06-01' and '2016-12-31';
"""

q2 = """

Select Category, avg(PurchasePrice) from pu 
left join cu on cu.CustomerID==pu.CustomerID left join pr on pu.ProductID==pr.ProductID
GROUP by cu.CustomerID
HAVING COUNT(DISTINCT pu.ProductID)>=3
"""

q3 = """
Select ProductName FROM (
Select Category, ProductName, PurchasePrice from pu left join pr
on pu.ProductID==pr.ProductID
GROUP by pr.Category, pr.ProductName)
GROUP BY Category
HAVING MAX(PurchasePrice)
"""

fh = pu[(pu['PurchaseDate']>= date(2016,1,1)) & (pu['PurchaseDate']<=date(2016,6,30))]
sh = pu[(pu['PurchaseDate']>= date(2016,7,1)) & (pu['PurchaseDate']<=date(2016,12,31))]
df1 = pysqldf(q)
df2 = pysqldf(q1)
df3 = pysqldf(q2)
df4 = pysqldf(q3)
print(df1, df2, df3, df4)

df5 = pd.merge(fh,pr, on='ProductID').groupby('Category')['PurchasePrice'].sum()
df6 = pd.merge(sh,pr, on='ProductID').groupby('Category')['PurchasePrice'].sum()

df2.plot(kind='line', label='First half')
df3.plot(kind='line', label='Second half')
plt.legend()
plt.ylabel('Sales(sum of ProductPrices)')
plt.show()

