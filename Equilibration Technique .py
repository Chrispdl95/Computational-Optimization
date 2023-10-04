#!/usr/bin/env python
# coding: utf-8

# In[1]:


def mps_to_txt_matrixes(file_name):
    import numpy as np
    f = open(file_name+'.mps') 
    
    x=[]
    EQin=[]
    MinMax= -1
    for i in f:
        splitted= i.split()
        x.append(splitted)
        flag =0
    for i in range(len(x)):
        if x[i][0]== 'ROWS' and flag == 0 :
            flag += 1
            row=i #where "ROWS"
        elif  x[i][0] == 'COLUMNS' and flag == 1:
            flag += 1
            colum= i #where "COLUMNS"
        elif x[i][0] == 'RHS' and flag == 2:
            flag += 1
            rhs = i #where rhs starts
        elif 'ENDATA' in x[i][0]:
            flag=4 
            end= i 
    # find the name of the objective function and append the EQin vector
    for i in range(2,colum):
        if x[i][0]== 'L':
            EQin.append(-1)
        elif x[i][0]== 'G':
            EQin.append(1)
        elif x[i][0]== 'E':
            EQin.append(0)
        else :
            name_objective= x[i][1]
        
    constraints=[]
    for i in range(row+2,colum):
        if x[i][1] not in constraints:
            constraints.append(x[i][1])
        
    variables=[]
    for i in range(colum+1,rhs):
        if (x[i][0]) not in variables:
            variables.append(x[i][0])
    #number of constraints
    num_constraints = len(constraints)
    
    #number of variables
    num_variables= len(variables)
    
    #create A zero matrix mxn(m= constraints and n = variables)
    A= np.zeros((num_constraints, num_variables))
    #create empty c array
    c = np.zeros((num_variables,), dtype=float)
    for i in range(colum+1, rhs):
        a= int(x[i][0][3:])
        for y in range(1,len(x[i]),2):
            #print(x[i][y])
            if x[i][y]== name_objective:
                c[a-1]+= float(x[i][y+1])
            elif y==1 or y==3:
                b= int(x[i][y][3:])
                A[b-1,a-1] +=  float(x[i][y+1])
        
        
    # b (1xm) 
    b = np.zeros((num_constraints,),dtype=float)  

    for i in range(rhs+1,end):
        for y in range(len(x[i])):
            if y==1 or y==3 :
                a = int(x[i][y][3:])
                
                b[a-1] +=float(x[i][y+1])
    
    return A, b ,c ,EQin

def equilibration(A,b,c,EQin):
    import numpy
    index= list(range(len(A)))
    m = len(A) #number of constraints
    n = len(A[0]) #number of variable
    col_max= []  # stores the column wise maximas
    col_multi= []  #stores the column multiplier
    indexes= list(range(len(A))) # stores the indexes(rows) to iterate through in the second loop
    for col in range(n):  # iterate over all columns
        max_in_col = abs(A[0][col])  # assume the first element of the column(the top most) is the maximum
        index=0
        for row in range(1, m):  # iterate over the column(top to down)
                if abs(A[row][col])> max_in_col:
                    max_in_col = abs(A[row][col])
                    index=row
        indexes=list(filter(lambda a: a != index, indexes))        
        col_max.append(max_in_col)
        col_multi.append(1/max_in_col)
    if col_multi !=0:
        A=A*col_multi
        c=c*col_multi
    
    for row in indexes:
        max_in_row=abs(A[row][0]) # assume the first element of the rowis the maximum
        for col in range(1,n): #iterate over the row
            if abs(A[row][col])> max_in_row:
                max_in_row = abs(A[row][col])
       
        if max_in_row !=0:
            A[row]= A[row]*1/max_in_row
            b[row]=b[row]*1/max_in_row
    return A,b,c,EQin

