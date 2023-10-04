#!/usr/bin/env python
# coding: utf-8

# In[1]:


def compressed_sparse_column(A):
    import numpy as np
    Anz=[]
    JA=[]
    IA=np.zeros(len(A[0])+1)+1
    for i in range(len(A[0])):
        l=0 #number of non zeros in a column
        for j in range(len(A)): 
            if A[j,i]!=0:
                Anz.append(A[j,i])
                JA.append(j+1)
                l+=1
                
        if l==0:
            IA[i+1]=IA[i]
        else:
            IA[i+1]=IA[i]+l
    return Anz, JA , IA

