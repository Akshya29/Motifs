# TIGRESS
GENIE3 is an ensemble algorithm but differs from TIGRESS in that it uses a non-linear tree-based method for feature selection, while TIGRESS uses LARS;

Trustful Inference of Gene REgulation using Stability Selection (TIGRESS) is a model that combines stability selection and least angle regression (LARS), to infer GRNs.

It depends on the scoring method, the numberR of resampling runs, the randomization factor α and the number of LARS stepsL.

TIGRESS treats the expression levels of TFs as predictors and the expression of a target gene as the response. It applies LARS to gradually add TFs (predictors) that best explain the target gene, mimicking the forward selection process. TIGRESS repeats this process several times, thus avoiding overfitting and providing higher accuracy. Furthermore, it was ranked in the top 3 GRN inference methods at the 2010 DREAM5 challenge 
