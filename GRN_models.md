Recently, many machine learning–based models have been developed to infer gene regulatory networks (GRNs), which represent how genes regulate each other. While these approaches can provide valuable biological insights, they often yield different predictions when applied to the same dataset, making it difficult to confidently identify regulatory interactions. Additionally, experimental noise and the inherent complexity of gene regulation — which can be nonlinear, context-dependent, and include feedback loops — further challenge accurate modeling. To overcome these issues, integrating predictions from multiple methods has been shown to improve overall accuracy compared to relying on a single approach. This strategy, which combines different algorithms to generate consensus networks, leverages the unique strengths of each method, resulting in more robust and biologically meaningful GRNs.

The bioNeRo package facilitates this process by integrating three popular models — GENIE3, ARACNe, and CLR — to predict GRNs for any organism. All that is required are gene expression data and a list of transcription factors.
# GENIE3
GENIE3 (GEne Network Inference with Ensemble of Trees), developed by(Huynh-Thu et al., 2010) is a machine learning-based algorithm that infers gene regulatory networks (GRNs) from high-dimensional gene expression data. It utilizes ensemble methods—specifically Random Forests and Extra-Trees—to model complex regulatory relationships without making strong assumptions about the underlying data. 

# CLR
The Context Likelihood of Relatedness (CLR) is a computational method designed to infer gene regulatory networks (GRNs) by analyzing gene expression data.

CLR computes the mutual information (MI) between the expression levels of every possible regulator-target gene pair. This approach is particularly effective for high-dimensional datasets generated through techniques like microarray and RNA-Seq, which simultaneously capture the expression levels of thousands of genes.

# ARACNe
Like CLR, it computes pairwise mutual between gene expression profiles to identify statistical dependencies. Additionally, ARACNe eliminates the indirect interactions (φ ij = 0) using Data Processing Inequality (DPI), which helps to retain mostly direct regulatory interactions and reduce false positives due to indirect relationships. 

# References
Huynh-Thu, V. A., Irrthum, A., Wehenkel, L., & Geurts, P. (2010). Inferring regulatory networks from expression data using tree-based methods. PloS one, 5(9), e12776. 

Margolin, A. A., Nemenman, I., Basso, K., Wiggins, C., Stolovitzky, G., Favera, R. D., & Califano, A. (2006). ARACNE: an algorithm for the reconstruction of gene regulatory networks in a mammalian cellular context. BMC bioinformatics, 7(Suppl 1), S7. 

Faith, J. J., Hayete, B., Thaden, J. T., Mogno, I., Wierzbowski, J., Cottarel, G., Kasif, S., Collins, J. J., & Gardner, T. S. (2007). Large-scale mapping and validation of Escherichia coli transcriptional regulation from a compendium of expression profiles. PLoS biology, 5(1), e8. 

Almeida-Silva, F., & Venancio, T. M. (2025). Gene regulatory network inference. BioNERO vignette 02. Retrieved from http://bioconductor.org/packages/devel/bioc/vignettes/BioNERO/inst/doc/vignette_02_GRN_inference.html


