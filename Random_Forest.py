#packages required
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import roc_auc_score, average_precision_score, confusion_matrix, auc
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, classification_report
from sklearn.metrics import roc_curve, precision_recall_curve
from sklearn.cluster import KMeans

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

#Random Forest classifier
rf_clf = RandomForestClassifier(n_estimators=500, class_weight="balanced", random_state=42, n_jobs=8 ) #500
rf_clf.fit(X_train, y_train)

y_pred = rf_clf.predict(X_test)
rf_prob = rf_clf.predict_proba(X_test)[:, 1]  # probabilities for ROC

#Evaluate 
roc = roc_auc_score(y_test, rf_prob)
precision, recall, _ = precision_recall_curve(y_test, rf_prob)
pr_auc = auc(recall, precision)

# Classification report
print("\nModel performance:")
print(f"ROC-AUC: {roc:.4f}")
print(f"PR-AUC: {pr_auc:.4f}")
print(classification_report(y_test, (rf_prob>0.5).astype(int)))

# Feature importance 
importances = pd.Series(rf_clf.feature_importances_, index=X_train.columns)

# Drop 'has_dap' and 'all_evidence' before sorting/printing. This is done because they are just a combination of features that already exist.
# they are required only for training the model; looking at their importance score is not necessary
importances_filtered = importances.drop(['has_dap', 'has_evidence'], errors='ignore').sort_values(ascending=False)

print("\nFeature importance (excluding has_dap and all_evidence):\n", importances_filtered)

# classification report at different thresholds to identify the best one
for t in [0.4, 0.5, 0.6, 0.7, 0.8]:
    y_pred_t = (rf_prob > t).astype(int)
    print(f"\nThreshold {t}:")
    print(classification_report(y_test, y_pred_t, digits=3))

# to find the precision at each k = top 100,500,1000, and 5000
preds = pd.DataFrame({'prob': rf_prob, 'label': y_test})
preds = preds.sort_values('prob', ascending=False)
topk = [100, 500, 1000, 5000]
for k in topk:
    prec_k = preds.head(k)['label'].mean()
    print(f"Precision@{k}: {prec_k:.3f}")

# Predict on the remaining unlabelled data
# Prepare X_unlabeled
X_unlabeled = unlabeled[features].copy()
# Apply log transform (consistent with training)
X_unlabeled['p-value'] = np.log10(X_unlabeled['p-value'] + 1e-10)
# Fill missing and scale score features
X_unlabeled = X_unlabeled.fillna(0)
X_unlabeled[score_features] = scaler.transform(X_unlabeled[score_features])
# Predict
unlabeled['predicted_prob'] = rf_clf.predict_proba(X_unlabeled)[:, 1]
unlabeled['predicted_label'] = (unlabeled['predicted_prob'] > 0.5).astype(int)
# Summary
print(unlabeled['predicted_label'].value_counts())
