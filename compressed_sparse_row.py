#!/usr/bin/env python
# coding: utf-8

# In[5]:


def compressed_sparse_row(A):
    import numpy as np
    Anz=[]
    JR=[]
    JC=np.zeros(len(A)+1)+1
    for i in range(len(A)):
        l=0 #number of non zeros in a row
        for j in range(len(A[i])): 
            if A[i,j]!=0:
                Anz.append(A[i,j])
                JR.append(j+1)
                l+=1
        if l==0:
            JC[i+1]=JC[i]
        else:
            JC[i+1]=JC[i]+l
    return Anz, JR , JC

