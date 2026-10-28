import os, glob, sys, joblib, numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from features import load_wav, extract_features, LABELS

root = "data/real" if os.path.isdir("data/real") else "data/demo"
print("Training on:", root)
X, y = [], []
for idx, cls in enumerate(LABELS):
    for f in glob.glob(f"{root}/{cls}/*.wav"):
        X.append(extract_features(load_wav(f))[0])
        y.append(idx)
X, y = np.array(X), np.array(y)
if len(X) < 30:
    sys.exit("Not enough clips. Run generate_demo_data.py first.")

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=0)
model = RandomForestClassifier(n_estimators=300, random_state=0)
cv = cross_val_score(model, Xtr, ytr, cv=5)
print(f"5-fold CV accuracy : {cv.mean():.1%} (+/- {cv.std():.1%})")
model.fit(Xtr, ytr)
pred = model.predict(Xte)
print(f"Held-out test acc  : {(pred == yte).mean():.1%}")
print(classification_report(yte, pred, target_names=LABELS))
print("Confusion matrix:")
print(confusion_matrix(yte, pred))
if root.endswith("demo"):
    print("NOTE: This is SYNTHETIC data. About 100 percent is expected and is NOT a real result.")
os.makedirs("models", exist_ok=True)
joblib.dump({"model": model, "source": root, "test_acc": float((pred == yte).mean())},
            "models/dhwanisetu_rf.joblib")
print("Model saved -> models/dhwanisetu_rf.joblib")