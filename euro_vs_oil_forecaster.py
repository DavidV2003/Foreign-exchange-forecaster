# -*- coding: utf-8 -*-
"""Euro_vs_Dollar_Forecaster.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1icOKU6XuExcE4nMhifmpkXqTuM4lj7z_

# **Global**
"""

# Commented out IPython magic to ensure Python compatibility.

from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_blobs
from google.colab import drive
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics 
from sklearn import linear_model, neighbors
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
import matplotlib.pyplot as plt
import random


drive.mount('/content/gdrive')
# %cd '/content/gdrive/MyDrive/Bootcamp/Brayan_montenegro/EUR_OIL's
def normalize(x):               
    # it can also be done by using the scypy (stats) zscore
    mean = np.mean(x)#media
    sdeviation = np.std(x)
    y = (x-mean)/sdeviation
    return y

fecha=np.arange(1,4000)

eur = pd.read_csv('Datos históricos USD_EUR.csv',sep=";")
eur['fecha']=fecha
eur['ultimo']=normalize(eur['ultimo'])
eur=eur[['fecha','ultimo','apertura','maximo','minimo','var']]


oil = pd.read_csv('Datos históricos Futuros petróleo crudo WTI.csv',sep=";",)
oil['fecha']=fecha
oil['ultimo']=normalize(oil['ultimo'])
oil=oil[['fecha','ultimo','apertura','maximo','minimo','var']]


fig, ax=plt.subplots(figsize=(15,12))
for c,y,lb in zip(['r','b'],[eur['ultimo'],oil['ultimo']],['Euro','Oil']):
  ax.plot(fecha,y,linestyle='-',c=c,label=lb)
ax.legend()

"""# **Euro**

## Lineal
"""

#Lineal

#Librerias
from sklearn import cluster
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics.cluster import adjusted_rand_score, normalized_mutual_info_score, silhouette_score, homogeneity_score
from sklearn import linear_model

#Funcion de graficacion
def plot(data2D, target1D, predict1D, labels,cl):
    axs[0].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    axs[1].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    #Si aumentan los grupos debo hacer mas elif

    clr=['b','g','y','c','m','y','r']
  
    axs[0].plot(data2D, predict1D,c=clr[cl], label='Prediction')
    axs[1].scatter(i,y_pred_c[0],c=clr[cl])
    axs[0].set_title('Lineal, '+ str(labels))
    axs[0].grid()
    axs[1].set_title('Lineal, '+ str(labels))
    axs[1].grid()
    return

#Variables
y = eur['ultimo']
X = fecha[:, np.newaxis] 

epc=100
pend=[]
inter=[]

for i in range(1,4001,epc):
    lineal = linear_model.LinearRegression()
    lineal.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    pend.append(float(lineal.coef_))
    inter.append(float(lineal.intercept_))
    y_pred = lineal.predict(X[(i+epc)-epc:(i+epc)-1])
    



fig,axs = plt.subplots(1,4, figsize=(15,4))
#Mas variables
cluster_v=[]
inter=np.array(inter)
pend=np.array(pend)

#Cluster
axs[0].scatter(inter,pend)
axs[0].set_title('original')
N_class = 2



nom = ['KMeans', 'AgglomerativeClustering','DBSCAN']

cluster_methodos = [KMeans(n_clusters=N_class,max_iter=500,init='random'),
                    AgglomerativeClustering(n_clusters=N_class),
                    DBSCAN(eps=1,min_samples=N_class)]
inter=inter[:, np.newaxis] 
for f, c_m,n in zip(range(3),cluster_methodos,nom):
  cluster=c_m.fit_predict(inter)
  axs[f+1].scatter(inter,pend, c=cluster)
  axs[f+1].set_title(format(n))
  print(c_m.__class__.__name__)
  cluster_v.append(cluster)

#Plot con colores

for m in range (len(cluster_v)):
  fig, axs = plt.subplots(2,1,figsize=(30,6))
  for i, c in zip(range(1,4001,epc),cluster_v[m]):
    lineal_c = linear_model.LinearRegression()
    lineal_c.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    y_pred_c = lineal_c.predict(X[(i+epc)-epc:(i+epc)-1])
    plot(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1], y_pred_c,nom[m],c)

"""## Vecinos"""

#Vecinos
from sklearn import neighbors

def plotv(data2D, target1D, predict1D):
    plt.figure(figsize=(30, 6))
    plt.plot(data2D, target1D, 'y.', markersize=6, label='Samples')
    plt.plot(data2D, predict1D, 'k-', label='Prediction')
    plt.legend()
    plt.title('Neighbors: '+str(n))
    plt.grid()
    plt.show()
    return

n=30

y = eur['ultimo']
X = fecha[:, np.newaxis]  

neigh = neighbors.KNeighborsRegressor(n_neighbors=n)
neigh.fit(X, y)
#print("Slope: "+str(neigh.coef_)+", intercept:"+str(neigh.intercept_))
y_pred = neigh.predict(X)
plotv(X, y, y_pred)

"""## Gausiano"""

#Gausiano
fig, axs = plt.subplots(figsize=(30,6))
def plot(data2D, target1D, predict1D, i, labels):
    axs.plot(data2D, target1D, 'y.', markersize=6,
                           label='Samples')
    axs.plot(data2D, predict1D, 'k-', label='Prediction')
    axs.set_title('Gausiano, '+ str(labels))
    axs.grid()
    return

y = eur['ultimo']
X = fecha[:, np.newaxis] 
labels='Euro'

for i in range(1,4001,epc):
    gp = GaussianProcessRegressor(alpha=0.5)
    gp.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    #print("Slope: "+str(lasso.coef_)+", intercept: "+str(lasso.intercept_))
    y_pred = gp.predict(X[(i+epc)-epc:(i+epc)-1])
    plot(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1], y_pred, i,labels)

"""## Rigde"""

#Ridge

#Librerias
from sklearn import cluster
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics.cluster import adjusted_rand_score, normalized_mutual_info_score, silhouette_score, homogeneity_score
from sklearn import linear_model

#Funcion de graficacion
def plot(data2D, target1D, predict1D, labels,cl):
    axs[0].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    axs[1].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    #Si aumentan los grupos debo hacer mas elif

    clr=['b','g','y','c','m','y','r']
  
    axs[0].plot(data2D, predict1D,c=clr[cl], label='Prediction')
    axs[1].scatter(i,y_pred_c[0],c=clr[cl])
    axs[0].set_title('Lasso, '+ str(labels))
    axs[0].grid()
    axs[1].set_title('Lasso, '+ str(labels))
    axs[1].grid()
    return

#Variables
y = eur['ultimo']
X = fecha[:, np.newaxis] 

epc=100
pend=[]
inter=[]


for i in range(1,4001,epc):
    ridge = linear_model.Ridge(alpha=0.5)
    ridge.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    pend.append(float(ridge.coef_))
    inter.append(float(ridge.intercept_))
    y_pred = ridge.predict(X[(i+epc)-epc:(i+epc)-1])
    



fig,axs = plt.subplots(1,4, figsize=(15,4))
#Mas variables
cluster_v=[]
inter=np.array(inter)
pend=np.array(pend)

#Cluster
axs[0].scatter(inter,pend)
axs[0].set_title('original')
N_class = 2



nom = ['KMeans', 'AgglomerativeClustering','DBSCAN']

cluster_methodos = [KMeans(n_clusters=N_class,max_iter=500,init='random'),
                    AgglomerativeClustering(n_clusters=N_class),
                    DBSCAN(eps=8.679,min_samples=N_class)]
inter=inter[:, np.newaxis] 
for f, c_m,n in zip(range(3),cluster_methodos,nom):
  cluster=c_m.fit_predict(inter)
  axs[f+1].scatter(inter,pend, c=cluster)
  axs[f+1].set_title(format(n))
  print(c_m.__class__.__name__)
  cluster_v.append(cluster)

#Plot con colores

for m in range (len(cluster_v)):
  fig, axs = plt.subplots(2,1,figsize=(30,6))
  for i, c in zip(range(1,4001,epc),cluster_v[m]):

    ridge_c = linear_model.Ridge(alpha=0.5)
    ridge_c.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    y_pred_c = ridge_c.predict(X[(i+epc)-epc:(i+epc)-1])
    plot(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1], y_pred_c,nom[m],c)

"""## Lasso"""

#Lasso


#Librerias
from sklearn import cluster
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics.cluster import adjusted_rand_score, normalized_mutual_info_score, silhouette_score, homogeneity_score
from sklearn.linear_model import Lasso

#Funcion de graficacion
def plot(data2D, target1D, predict1D, labels,cl):
    axs[0].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    axs[1].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    #Si aumentan los grupos debo hacer mas elif

    clr=['b','g','y','c','m','y','r']
  
    axs[0].plot(data2D, predict1D,c=clr[cl], label='Prediction')
    axs[1].scatter(i,y_pred_c[0],c=clr[cl])
    axs[0].set_title('Lasso, '+ str(labels))
    axs[0].grid()
    axs[1].set_title('Lasso, '+ str(labels))
    axs[1].grid()
    return

#Variables
y = eur['ultimo']
X = fecha[:, np.newaxis]  

epc=100
pend=[]
inter=[]

#Guardar valores de intercept y slope

for i in range(1,4001,epc):
    lasso = Lasso(alpha=0.0001)
    lasso.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    pend.append(float(lasso.coef_))
    inter.append(float(lasso.intercept_))
    y_pred = lasso.predict(X[(i+epc)-epc:(i+epc)-1])
    



fig,axs = plt.subplots(1,4, figsize=(15,4))
#Mas variables
cluster_v=[]
inter=np.array(inter)
pend=np.array(pend)

#Cluster
axs[0].scatter(inter,pend)
axs[0].set_title('original')
N_class = 2



nom = ['KMeans', 'AgglomerativeClustering','DBSCAN']

cluster_methodos = [KMeans(n_clusters=N_class,max_iter=500,init='random'),
                    AgglomerativeClustering(n_clusters=N_class),
                    DBSCAN(eps=8.679,min_samples=N_class)]
inter=inter[:, np.newaxis] 
for f, c_m,n in zip(range(3),cluster_methodos,nom):
  cluster=c_m.fit_predict(inter)
  axs[f+1].scatter(inter,pend, c=cluster)
  axs[f+1].set_title(format(n))
  print(c_m.__class__.__name__)
  cluster_v.append(cluster)

#Plot con colores

for m in range (len(cluster_v)):
  fig, axs = plt.subplots(2,1,figsize=(30,6))
  for i, c in zip(range(1,4001,epc),cluster_v[m]):
    colors=np.ones(len(X[(i+epc)-epc:(i+epc)-1]))*c
    lasso_c = Lasso(alpha=0.0001)
    lasso_c.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    y_pred_c = lasso_c.predict(X[(i+epc)-epc:(i+epc)-1])
    plot(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1], y_pred_c,nom[m],c)

"""## Elastic"""

#Elastic

#Librerias
from sklearn import cluster
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics.cluster import adjusted_rand_score, normalized_mutual_info_score, silhouette_score, homogeneity_score
from sklearn.linear_model import ElasticNet

#Funcion de graficacion
def plot(data2D, target1D, predict1D, labels,cl):
    axs[0].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    axs[1].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    #Si aumentan los grupos debo hacer mas elif

    clr=['b','g','y','c','m','y','r']
  
    axs[0].plot(data2D, predict1D,c=clr[cl], label='Prediction')
    axs[1].scatter(i,y_pred_c[0],c=clr[cl])
    axs[0].set_title('Lasso, '+ str(labels))
    axs[0].grid()
    axs[1].set_title('Lasso, '+ str(labels))
    axs[1].grid()
    return

#Variables
y = eur['ultimo']
X = fecha[:, np.newaxis] 

epc=100
pend=[]
inter=[]

#Guardar valores de intercept y slope

for i in range(1,4001,epc):
    elastic = ElasticNet(alpha=0.0001)
    elastic.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    pend.append(float(elastic.coef_))
    inter.append(float(elastic.intercept_))
    y_pred = elastic.predict(X[(i+epc)-epc:(i+epc)-1])
    



fig,axs = plt.subplots(1,4, figsize=(15,4))
#Mas variables
cluster_v=[]
inter=np.array(inter)
pend=np.array(pend)

#Cluster
axs[0].scatter(inter,pend)
axs[0].set_title('original')
N_class = 2



nom = ['KMeans', 'AgglomerativeClustering','DBSCAN']

cluster_methodos = [KMeans(n_clusters=N_class,max_iter=500,init='random'),
                    AgglomerativeClustering(n_clusters=N_class),
                    DBSCAN(eps=8.679,min_samples=N_class)]
inter=inter[:, np.newaxis] 
for f, c_m,n in zip(range(3),cluster_methodos,nom):
  cluster=c_m.fit_predict(inter)
  axs[f+1].scatter(inter,pend, c=cluster)
  axs[f+1].set_title(format(n))
  print(c_m.__class__.__name__)
  cluster_v.append(cluster)

#Plot con colores

for m in range (len(cluster_v)):
  fig, axs = plt.subplots(2,1,figsize=(30,6))
  for i, c in zip(range(1,4001,epc),cluster_v[m]):
    colors=np.ones(len(X[(i+epc)-epc:(i+epc)-1]))*c
    ElasticNet_c = ElasticNet(alpha=0.0001)
    ElasticNet_c.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    y_pred_c = ElasticNet_c.predict(X[(i+epc)-epc:(i+epc)-1])
    plot(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1], y_pred_c,nom[m],c)

"""# **OIL**

## Lineal
"""

#Lineal

#Librerias
from sklearn import cluster
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics.cluster import adjusted_rand_score, normalized_mutual_info_score, silhouette_score, homogeneity_score
from sklearn import linear_model

#Funcion de graficacion
def plot(data2D, target1D, predict1D, labels,cl):
    axs[0].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    axs[1].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    #Si aumentan los grupos debo hacer mas elif

    clr=['b','g','y','c','m','y','r']
  
    axs[0].plot(data2D, predict1D,c=clr[cl], label='Prediction')
    axs[1].scatter(i,y_pred_c[0],c=clr[cl])
    axs[0].set_title('Lineal, '+ str(labels))
    axs[0].grid()
    axs[1].set_title('Lineal, '+ str(labels))
    axs[1].grid()
    return

#Variables
y = oil['ultimo']
X = fecha[:, np.newaxis] 

epc=100
pend=[]
inter=[]

for i in range(1,4001,epc):
    lineal = linear_model.LinearRegression()
    lineal.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    pend.append(float(lineal.coef_))
    inter.append(float(lineal.intercept_))
    y_pred = lineal.predict(X[(i+epc)-epc:(i+epc)-1])
    



fig,axs = plt.subplots(1,4, figsize=(15,4))
#Mas variables
cluster_v=[]
inter=np.array(inter)
pend=np.array(pend)

#Cluster
axs[0].scatter(inter,pend)
axs[0].set_title('original')
N_class = 2



nom = ['KMeans', 'AgglomerativeClustering','DBSCAN']

cluster_methodos = [KMeans(n_clusters=N_class,max_iter=500,init='random'),
                    AgglomerativeClustering(n_clusters=N_class),
                    DBSCAN(eps=8.679,min_samples=N_class)]
inter=inter[:, np.newaxis] 
for f, c_m,n in zip(range(3),cluster_methodos,nom):
  cluster=c_m.fit_predict(inter)
  axs[f+1].scatter(inter,pend, c=cluster)
  axs[f+1].set_title(format(n))
  print(c_m.__class__.__name__)
  cluster_v.append(cluster)

#Plot con colores

for m in range (len(cluster_v)):
  fig, axs = plt.subplots(2,1,figsize=(30,6))
  for i, c in zip(range(1,4001,epc),cluster_v[m]):

    lineal_c = linear_model.LinearRegression()
    lineal_c.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    y_pred_c = lineal_c.predict(X[(i+epc)-epc:(i+epc)-1])
    plot(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1], y_pred_c,nom[m],c)

"""## Vecinos"""

#Vecinos
from sklearn import neighbors

def plotv(data2D, target1D, predict1D):
    plt.figure(figsize=(30, 6))
    plt.plot(data2D, target1D, 'y.', markersize=6, label='Samples')
    plt.plot(data2D, predict1D, 'k-', label='Prediction')
    plt.legend()
    plt.title('Neighbors: '+str(n))
    plt.grid()
    plt.show()
    return

n=30


neigh = neighbors.KNeighborsRegressor(n_neighbors=n)
neigh.fit(X, y)
#print("Slope: "+str(neigh.coef_)+", intercept:"+str(neigh.intercept_))
y_pred = neigh.predict(X)
plotv(X, y, y_pred)

"""## Gausiano"""

#Gausiano
fig, axs = plt.subplots(figsize=(30,6))
def plot(data2D, target1D, predict1D, i, labels):
    axs.plot(data2D, target1D, 'y.', markersize=6,
                           label='Samples')
    axs.plot(data2D, predict1D, 'k-', label='Prediction')
    axs.set_title('Gausiano, '+ str(labels))
    axs.grid()
    return

labels='Oil'

for i in range(1,4001,epc):
    gp = GaussianProcessRegressor(alpha=0.5)
    gp.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    #print("Slope: "+str(lasso.coef_)+", intercept: "+str(lasso.intercept_))
    y_pred = gp.predict(X[(i+epc)-epc:(i+epc)-1])
    plot(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1], y_pred, i,labels)

"""## Rigde"""

#Ridge


#Librerias
from sklearn import cluster
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics.cluster import adjusted_rand_score, normalized_mutual_info_score, silhouette_score, homogeneity_score
from sklearn import linear_model

#Funcion de graficacion
def plot(data2D, target1D, predict1D, labels,cl):
    axs[0].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    axs[1].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    #Si aumentan los grupos debo hacer mas elif

    clr=['b','g','y','c','m','y','r']
  
    axs[0].plot(data2D, predict1D,c=clr[cl], label='Prediction')
    axs[1].scatter(i,y_pred_c[0],c=clr[cl])
    axs[0].set_title('Lasso, '+ str(labels))
    axs[0].grid()
    axs[1].set_title('Lasso, '+ str(labels))
    axs[1].grid()
    return

#Variables
y = oil['ultimo']
X = fecha[:, np.newaxis] 

epc=100
pend=[]
inter=[]


for i in range(1,4001,epc):
    ridge = linear_model.Ridge(alpha=0.5)
    ridge.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    pend.append(float(ridge.coef_))
    inter.append(float(ridge.intercept_))
    y_pred = ridge.predict(X[(i+epc)-epc:(i+epc)-1])
    



fig,axs = plt.subplots(1,4, figsize=(15,4))
#Mas variables
cluster_v=[]
inter=np.array(inter)
pend=np.array(pend)

#Cluster
axs[0].scatter(inter,pend)
axs[0].set_title('original')
N_class = 2



nom = ['KMeans', 'AgglomerativeClustering','DBSCAN']

cluster_methodos = [KMeans(n_clusters=N_class,max_iter=500,init='random'),
                    AgglomerativeClustering(n_clusters=N_class),
                    DBSCAN(eps=8.679,min_samples=N_class)]
inter=inter[:, np.newaxis] 
for f, c_m,n in zip(range(3),cluster_methodos,nom):
  cluster=c_m.fit_predict(inter)
  axs[f+1].scatter(inter,pend, c=cluster)
  axs[f+1].set_title(format(n))
  print(c_m.__class__.__name__)
  cluster_v.append(cluster)

#Plot con colores

for m in range (len(cluster_v)):
  fig, axs = plt.subplots(2,1,figsize=(30,6))
  for i, c in zip(range(1,4001,epc),cluster_v[m]):

    ridge_c = linear_model.Ridge(alpha=0.5)
    ridge_c.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    y_pred_c = ridge_c.predict(X[(i+epc)-epc:(i+epc)-1])
    plot(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1], y_pred_c,nom[m],c)

"""## Lasso"""

#Lasso

#Librerias
from sklearn import cluster
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics.cluster import adjusted_rand_score, normalized_mutual_info_score, silhouette_score, homogeneity_score
from sklearn.linear_model import Lasso

#Funcion de graficacion
def plot(data2D, target1D, predict1D, labels,cl):
    axs[0].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    axs[1].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    #Si aumentan los grupos debo hacer mas elif

    clr=['b','g','y','c','m','y','r']
  
    axs[0].plot(data2D, predict1D,c=clr[cl], label='Prediction')
    axs[1].scatter(i,y_pred_c[0],c=clr[cl])
    axs[0].set_title('Lasso, '+ str(labels))
    axs[0].grid()
    axs[1].set_title('Lasso, '+ str(labels))
    axs[1].grid()
    return


#Variables
y = oil['ultimo']
X = fecha[:, np.newaxis] 

epc=100
pend=[]
inter=[]

#Guardar valores de intercept y slope

for i in range(1,4001,epc):
    lasso = Lasso(alpha=0.0001)
    lasso.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    pend.append(float(lasso.coef_))
    inter.append(float(lasso.intercept_))
    y_pred = lasso.predict(X[(i+epc)-epc:(i+epc)-1])
    
    



fig,axs = plt.subplots(1,4, figsize=(15,4))
#Mas variables
cluster_v=[]
inter=np.array(inter)
pend=np.array(pend)

#Cluster
axs[0].scatter(inter,pend)
axs[0].set_title('original')
N_class = 2



nom = ['KMeans', 'AgglomerativeClustering','DBSCAN']

cluster_methodos = [KMeans(n_clusters=N_class,max_iter=500,init='random'),
                    AgglomerativeClustering(n_clusters=N_class),
                    DBSCAN(eps=8.68,min_samples=N_class)]
inter=inter[:, np.newaxis] 
for f, c_m,n in zip(range(3),cluster_methodos,nom):
  cluster=c_m.fit_predict(inter)
  axs[f+1].scatter(inter,pend, c=cluster)
  axs[f+1].set_title(format(n))
  print(c_m.__class__.__name__)
  cluster_v.append(cluster)

#Plot con colores


for m in range (len(cluster_v)):
  fig, axs = plt.subplots(2,1,figsize=(30,6))
  for i, c in zip(range(1,4001,epc),cluster_v[m]):
    lasso_c = Lasso(alpha=0.0001)
    lasso_c.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    y_pred_c = lasso_c.predict(X[(i+epc)-epc:(i+epc)-1])
    plot(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1], y_pred_c,nom[m],c)

"""## Elastic"""

#Elastic

#Librerias
from sklearn import cluster
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics.cluster import adjusted_rand_score, normalized_mutual_info_score, silhouette_score, homogeneity_score
from sklearn.linear_model import ElasticNet

#Funcion de graficacion
def plot(data2D, target1D, predict1D, labels,cl):
    axs[0].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    axs[1].plot(data2D, target1D, 'k-', markersize=6,
                           label='Samples')
    #Si aumentan los grupos debo hacer mas elif

    clr=['b','g','y','c','m','y','r']
  
    axs[0].plot(data2D, predict1D,c=clr[cl], label='Prediction')
    axs[1].scatter(i,y_pred_c[0],c=clr[cl])
    axs[0].set_title('Lasso, '+ str(labels))
    axs[0].grid()
    axs[1].set_title('Lasso, '+ str(labels))
    axs[1].grid()
    return

#Variables
y = oil['ultimo']
X = fecha[:, np.newaxis] 

epc=100
pend=[]
inter=[]

#Guardar valores de intercept y slope

for i in range(1,4001,epc):
    elastic = ElasticNet(alpha=0.0001)
    elastic.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    pend.append(float(elastic.coef_))
    inter.append(float(elastic.intercept_))
    y_pred = elastic.predict(X[(i+epc)-epc:(i+epc)-1])
    



fig,axs = plt.subplots(1,4, figsize=(15,4))
#Mas variables
cluster_v=[]
inter=np.array(inter)
pend=np.array(pend)

#Cluster
axs[0].scatter(inter,pend)
axs[0].set_title('original')
N_class = 2



nom = ['KMeans', 'AgglomerativeClustering','DBSCAN']

cluster_methodos = [KMeans(n_clusters=N_class,max_iter=500,init='random'),
                    AgglomerativeClustering(n_clusters=N_class),
                    DBSCAN(eps=8.679,min_samples=N_class)]
inter=inter[:, np.newaxis] 
for f, c_m,n in zip(range(3),cluster_methodos,nom):
  cluster=c_m.fit_predict(inter)
  axs[f+1].scatter(inter,pend, c=cluster)
  axs[f+1].set_title(format(n))
  print(c_m.__class__.__name__)
  cluster_v.append(cluster)

#Plot con colores

for m in range (len(cluster_v)):
  fig, axs = plt.subplots(2,1,figsize=(30,6))
  for i, c in zip(range(1,4001,epc),cluster_v[m]):
    colors=np.ones(len(X[(i+epc)-epc:(i+epc)-1]))*c
    ElasticNet_c = ElasticNet(alpha=0.0001)
    ElasticNet_c.fit(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1])
    y_pred_c = ElasticNet_c.predict(X[(i+epc)-epc:(i+epc)-1])
    plot(X[(i+epc)-epc:(i+epc)-1], y[(i+epc)-epc:(i+epc)-1], y_pred_c,nom[m],c)
