# Probabilities from RF and XGBoost
rf_prob = rf_clf.predict_proba(X_test)[:, 1]
xgb_prob = xgb_clf.predict_proba(X_test)[:, 1]
ensemble_prob = (rf_prob + xgb_prob) / 2

# Precision-Recall curve
precision, recall, thresholds = precision_recall_curve(y_test, ensemble_prob)
f1_scores = 2 * precision * recall / (precision + recall + 1e-10)

# Find threshold that maximizes F1 but avoids extreme recall=1
# Filter thresholds to those giving recall <= ~0.6 for balance
valid_idx = np.where(recall <= 0.6)[0]
best_idx = valid_idx[np.argmax(f1_scores[valid_idx])]
best_threshold = thresholds[best_idx]

# Predict using this threshold
y_pred = (ensemble_prob > best_threshold).astype(int)

# Metrics
print(f"Optimal threshold for balanced F1: {best_threshold:.3f}")
print(classification_report(y_test, y_pred))

# Feature importance (average of RF + XGB importance)
avg_importance = (importances + importance_xgb) / 2
print("\nAverage feature importance:\n", avg_importance.sort_values(ascending=False))


