import pandas as pa
import numpy as np
from scipy.sparse import csr_matrix, isspmatrix
from MICTI import Micti

def MICTI(sparceMatrix,geneNames,cellNames,k=None,cluster_assignment=None, th=0,seed=None, ensembel=False, organisum="hsapiens"):
    #check sparcity of the matrix
    if(sparceMatrix.shape[0]!=len(cellNames)):
        print("The number of cells and the given cell names does not match")
        sys.exit()
    elif(sparceMatrix.shape[1]!=len(geneNames)):
        print("The number of genes and the given gene names does not match")
        sys.exit()
    else:
        #check cluster assignment if it is provided by the user
        if(cluster_assignment is not None):
            if(len(cluster_assignment)!=len(cellNames)):
                print("the number of cells and cluster assignment does not match")
                sys.exit()
            else:
                labelMatrix=pa.get_dummies(cluster_assignment)
                labelArray=np.argwhere(np.array(labelMatrix))[:,1]
                kk=len(set(labelArray))
                cluster_labels=list(set(labelMatrix.columns))
        else:
            labelArray=None
            cluster_labels=None
            kk=k
        #change to sparce matrix if the data is not in a sparce matrix format        
        if not isspmatrix(sparceMatrix):
            sparceMatrix=csr_matrix(sparceMatrix)
        #creat micti object
        micti_obj=Micti(sparceMatrix,geneNames,cellNames,k=kk,cluster_label=cluster_labels,cluster_assignment=labelArray, th=th,seed=seed, ensembel=ensembel, organisum=organisum)
    return micti_obj

