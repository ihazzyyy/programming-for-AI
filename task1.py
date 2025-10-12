import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

train_data = pd.read_csv(r"C:\Users\lenovo\Desktop\train.csv")
test_data = pd.read_csv(r"C:\Users\lenovo\Desktop\test.csv")

y = np.log1p(train_data["SalePrice"]) 
X = train_data.drop("SalePrice", axis=1)

numeric_features = X.select_dtypes(include=["int64", "float64"]).columns
categorical_features = X.select_dtypes(include=["object"]).columns

preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

model = XGBRegressor(
    n_estimators=1200,      
    learning_rate=0.05,       
    max_depth=6,             
    subsample=0.8,           
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline(steps=[("preprocessor", preprocessor),
                           ("model", model)])

X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)


pipeline.fit(X_train, y_train)

preds_valid = pipeline.predict(X_valid)
preds_valid_real = np.expm1(preds_valid)
y_valid_real = np.expm1(y_valid)

mae = mean_absolute_error(y_valid_real, preds_valid_real)
rmse = mean_squared_error(y_valid_real, preds_valid_real)
r2 = r2_score(y_valid_real, preds_valid_real)

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R² Score (Accuracy): {r2:.4f}")

test_preds = pipeline.predict(test_data)
test_preds_real = np.expm1(test_preds)

output = pd.DataFrame({
    "Id": test_data["Id"],
    "SalePrice": test_preds_real
})
output.to_csv("submission.csv", index=False)
print("Predictions saved to submission.csv")
