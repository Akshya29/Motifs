Gene regulatory networks (GRNs) were inferred using GENIE3, TIGRESS, ARACNe, and CLR, and the resulting network predictions were incorporated as feature columns. In addition, biological datasets capturing chromatin accessibility and regulatory potential were integrated, including Accessible Chromatin Regions (ACRs) (Zheng et al., 2025) and Unmethylated Regions (UMRs) (Crisp et al., 2020; Xu et al., 2022). These regions represent potential transcription factor (TF) binding sites, with UMRs frequently overlapping promoters and enhancers. To identify possible TF regulators, FIMO was applied to promoter sequences, ACRs, and UMRs, yielding an experimentally supported GRN. Furthermore, DAP-seq peak data from Yuan et al. (2024) were incorporated to provide additional evidence of TF–DNA interactions.

Three models —Random Forest, XGBoost, and an Ensemble model (averaged from both models) — were built using these GRNs as features to predict the best/accurate GRNs.

# REFERENCES
Crisp, P. A., Marand, A. P., Noshay, J. M., Zhou, P., Lu, Z., Schmitz, R. J., & Springer, N. M. (2020). Stable unmethylated DNA demarcates expressed genes and their cis-regulatory space in plant genomes. Proceedings of the National Academy of Sciences, 117(38), 23991-24000.

Xu, Q., Wu, L., Luo, Z., Zhang, M., Lai, J., Li, L., Springer, N. M., & Li, Q. (2022). DNA demethylation affects imprinted gene expression in maize endosperm. Genome biology, 23(1), 77.

Yuan, Y., Huo, Q., Zhang, Z., Wang, Q., Wang, J., Chang, S., Cai, P., Song, K. M., Galbraith, D. W., & Zhang, W. (2024). Decoding the gene regulatory network of endosperm differentiation in maize. Nature communications, 15(1), 34.

Zheng, G. M., Wu, J. W., Li, J., Zhao, Y. J., Zhou, C., Ren, R. C., Wei, Y. M., Zhang, X. S., & Zhao, X. Y. (2025). The chromatin accessibility landscape during early maize seed development. The Plant Journal, 121(6), e70073.



