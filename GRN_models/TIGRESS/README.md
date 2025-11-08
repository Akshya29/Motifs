# TIGRESS
GENIE3 is an ensemble-based algorithm that infers gene regulatory networks (GRNs) using a non-linear, tree-based approach for feature selection. In contrast, TIGRESS (Trustful Inference of Gene REgulation using Stability Selection) employs a linear regression framework that combines stability selection with Least Angle Regression (LARS) to identify regulatory relationships.

TIGRESS treats the expression levels of transcription factors (TFs) as predictors and the expression of each target gene as the response variable. The method applies LARS to iteratively add TFs that best explain the target gene’s expression, effectively performing a forward-selection process. This procedure is repeated multiple times under different randomizations, controlled by parameters such as the scoring method, the number of resampling runs, the randomization factor (α), and the number of LARS steps (L). Through stability selection, TIGRESS mitigates overfitting and enhances robustness. Notably, TIGRESS ranked among the top three GRN inference methods in the DREAM5 network inference challenge (Marbach et al., 2012).

However, TIGRESS is based on Least Angle Regression (LARS), a linear model. This means it cannot effectively capture non-linear or complex gene–gene interactions, which are common in biological systems. Additionally, like many GRN inference methods, TIGRESS typically operates on steady-state (non-time-series) expression data. It therefore cannot model dynamic or temporal regulatory changes.

# REFERENCES
Marbach, D., Costello, J. C., Küffner, R., Vega, N. M., Prill, R. J., Camacho, D. M., Allison, K. R., Kellis, M., & Collins, J. J. (2012). Wisdom of crowds for robust gene network inference. Nature methods, 9(8), 796-804

Haury, A. C., Mordelet, F., Vera-Licona, P., & Vert, J. P. (2012). TIGRESS: trustful inference of gene regulation using stability selection. BMC systems biology, 6(1), 145.
