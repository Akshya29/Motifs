#packages
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from boruta import BorutaPy
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler  # Import StandardScaler
from sklearn.metrics import roc_auc_score, average_precision_score, confusion_matrix, auc
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, classification_report
from sklearn.metrics import roc_curve, precision_recall_curve
from xgboost import XGBClassifier

TRUE_POSITIVES #gold_standard
DATA #integrated data

TRUE_POSITIVES #gold_standard/ ChIP-seq data
DATA #integrated GRNs

# Create TP set
tp_set = set(TRUE_POSITIVE[['TF', 'Target']].apply(tuple, axis=1))

# Identify true positives in DATA
tp_mask = DATA[['TF', 'Target']].apply(tuple, axis=1).isin(tp_set)
tp = DATA[tp_mask].copy()
tp['label'] = 1

# Only consider TFs that exist in TRUE_POSITIVE
valid_tfs = set(TRUE_POSITIVE['TF'])

# Potential negatives = same TFs, but Targets not in TRUE_POSITIVE for that TF
tp_dict = TRUE_POSITIVE.groupby('TF')['Target'].apply(set).to_dict()

def is_valid_negative(row):
    tf, target = row['TF'], row['Target']
    return tf in valid_tfs and target not in tp_dict.get(tf, set())

potential_negatives = DATA[DATA.apply(is_valid_negative, axis=1)].copy()

# Sample negatives (3x number of positives)
n_tp = len(tp)
n_tn = n_tp * 3
negatives = potential_negatives.sample(n=min(n_tn, len(potential_negatives)), random_state=42)
negatives['label'] = 0

# Combine labeled data
labeled = pd.concat([tp, negatives], ignore_index=True)

# Remaining data = unlabeled set
labeled_pairs = set(labeled[['TF', 'Target']].apply(tuple, axis=1))
unlabeled = DATA[~DATA[['TF', 'Target']].apply(tuple, axis=1).isin(labeled_pairs)].copy().reset_index(drop=True)


# Summary
print(f"Positives (TP): {len(tp)}") #57,743
print(f"Negatives (sampled TN): {len(negatives)}") #173,229
print(f"Unlabeled remaining: {len(unlabeled)}") #14,001,908
print(labeled['label'].value_counts(normalize=True))
# 0   0.75
# 1   0.25

labeled['p-value'] = pd.to_numeric(labeled['p-value'], errors='coerce')
# Replace missing or zero p-values with 1.0 (non-significant)
labeled['p-value'] = labeled['p-value'].fillna(1.0)
labeled['p-value'] = np.clip(labeled['p-value'], 1e-10, 1.0)

# log-transform
labeled['p-value'] = -np.log10(labeled['p-value'])

score_features = ['p-value', 'Genie3Score', 'AracneScore', 'ClrScore', 'TigressScore']
binary_features = ['ACR', 'UMR', 'DAP_seq', 'has_dap', 'has_evidence']
features = score_features + binary_features

X = labeled[features].fillna(0)
y = labeled['label']

# Standaridize
scaler = StandardScaler()
X[score_features] = scaler.fit_transform(X[score_features])

# Split into 80-20% for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


# XGBoost Classifier
xgb_clf = XGBClassifier(
    n_estimators=1000,
    learning_rate=0.03,
    max_depth=4,
    subsample=0.9,
    colsample_bytree=0.8,
    min_child_weight=2,
    reg_alpha=0.3,
    reg_lambda=1.0,
    eval_metric='logloss',
    scale_pos_weight=np.sum(y_train == 0) / np.sum(y_train == 1),  # make positives more important
    random_state=42,
    n_jobs=8
)

xgb_clf.fit(X_train, y_train,)

# Predictions
prob = xgb_clf.predict_proba(X_test)[:, 1]

# Evaluate metrics
roc = roc_auc_score(y_test, prob)
precision, recall, thresholds = precision_recall_curve(y_test, prob)
pr_auc = auc(recall, precision)
y_pred_opt = (prob >= 0.5).astype(int)
print(classification_report(y_test, y_pred_opt))

print("\nModel performance:")
print(f"ROC-AUC: {roc:.4f}")
print(f"PR-AUC:  {pr_auc:.4f}")

# at different thresholds to find the best one
for t in [0.4, 0.5, 0.6, 0.7, 0.8]:
    y_pred_t = (prob > t).astype(int)
    print(f"\nThreshold {t}:")
    print(classification_report(y_test, y_pred_t, digits=3))

#feature importances
importances = pd.Series(xgb_clf.feature_importances_, index=X_train.columns)

# Drop 'has_dap' and 'all_evidence' before sorting/printing
importances_filtered = importances.drop(['has_dap', 'has_evidence'], errors='ignore').sort_values(ascending=False)

print("\nFeature importance (excluding has_dap and has_evidence):\n", importances_filtered)

# Predict in the remaining unlabeled data
X_unlabeled = unlabeled[features].copy()
# Apply log transform (consistent with training)
X_unlabeled['p-value'] = np.log10(X_unlabeled['p-value'] + 1e-10)
# Fill missing and scale score features
X_unlabeled = X_unlabeled.fillna(0)
X_unlabeled[score_features] = scaler.transform(X_unlabeled[score_features])
#Preduct
unlabeled['predicted_prob'] = xgb_clf.predict_proba(X_unlabeled)[:, 1]
unlabeled['predicted_label'] = (unlabeled['predicted_prob'] > 0.5).astype(int)

#check counts
print(unlabeled['predicted_label'].value_counts())
#predicted_label
# 0    9169334
# 1    4832574
