..

========================================================
MICTI- Marker gene Identification for Cell Type Identity
========================================================

Recent advances in single-cell gene expression profiling technology have revolutionized the understanding of molecular processes underlying developmental cell and tissue differentiation, enabling the discovery of novel cell types and molecular markers that characterize developmental trajectories.  Common approaches for identifying marker genes are based on pairwise statistical testing for differential gene expression between cell types in heterogeneous cell populations, which is challenging due to unequal sample sizes and variance between groups resulting in little statistical power and inflated type I errors. 

Introduction
============

We developed an alternative feature extraction method, *Marker gene Identification for Cell Type Identity* (**MICTI**), that encodes the cell type specific expression information to each gene in every single cell. This approach identifies features (genes) that are cell type specific for a given cell type in heterogeneous cell population.


Overview
========

To install the current release::

	pip install micti
	
How to use MICTI
================

Import MICTI::

	from MICTI import *

Creating MICTI object for known cell type cluster label::

	mictiObject=MICTI(dataset, geneName, cellName, cluster_assignment=cell_type_label)

2D visualisation with T-SNE::

	mictiObject.get_Visualization(method="tsne")

Get MICTI marker genes::

	mictiObject.get_markers_by_Pvalues_and_Zscore(cell_type, threshold_pvalue=.01)

Perfom unsupervised clustering(k-means or Gaussian mixture) on dataset for unknown cell types::

	mictiObject.cluster_cells(k, method="kmeans")

Perform gene list enrichment analysis::

	mictiObject.get_gene_list_over_representation_analysis(geneList)

Licence
=======

'MICTI LICENCE <https://github.com/insilicolife/micti/blob/master/LICENSE>'_
