# import math
# from pydantic import BaseModel
# from sklearn.ensemble import RandomForestRegressor
# import kagglehub
# import pandas as pd
# from matplotlib import pyplot as plt
# import seaborn as sns
# from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
# from xgboost import XGBClassifier
#
# from sklearn.model_selection import train_test_split, cross_val_score
# from sklearn.linear_model import LinearRegression, LogisticRegression
# from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, confusion_matrix, accuracy_score, \
#     precision_score
# from sklearn.preprocessing import LabelEncoder

# def train_plant_model():
#     # Download latest version
#     dataset_file_name = "plant_health_data.csv"
#     path = kagglehub.dataset_download("ziya07/plant-health-data") + "/" + dataset_file_name
#     df = pd.read_csv(path)
#
#     df = df.dropna()  # simple strategy; refine if needed
#
#     print("Loaded dataset at:", path)
#
#     # ensure data are sorted by plant ID and date
#     df = df.sort_values(['Plant_ID', 'Timestamp'])
#
#     # calculate height difference divided by elapsed days
#     df['Previous_Timestamp'] = df.groupby('Plant_ID')['Timestamp'].shift(1)
#     # days between measurements
#     df['Days_Elapsed'] = (pd.to_datetime(df['Timestamp']) -
#                           pd.to_datetime(df['Previous_Timestamp'])
#                           ).dt.days
#
#     encoder = LabelEncoder()
#     # df['Chlorpyll_Status'] = encoder.fit_transform(df['Chlorophyll_Content'])
#
#     # Independent Columns
#     features = ['Soil_Moisture', 'Ambient_Temperature',
#            'Soil_Temperature', 'Humidity', 'Light_Intensity', 'Soil_pH',
#            'Nitrogen_Level', 'Phosphorus_Level', 'Potassium_Level',
#            'Electrochemical_Signal']
#     X = df[features]
#
#     # Dependent Columns
#     y = df['Chlorophyll_Content']
#
#     X_train,X_test, y_train,y_test = train_test_split(X,y, test_size=0.2)
#
#     print("X_train Shape:", X_train.shape)
#     print("X_test Shape:", X_test.shape)
#     print("y_train Shape:", y_train.shape)
#     print("y_test Shape:", y_test.shape)
#
#     model = RandomForestRegressor(n_estimators=300, min_samples_leaf=5, random_state=42, n_jobs=-1)
#     model.fit(X_train, y_train)
#
#     pred = model.predict(X_test)
#     print("R2:", r2_score(y_test, pred), "MAE:", mean_absolute_error(y_test, pred))
#     print("CV R2:", cross_val_score(model, X, y, cv=5, scoring="r2").mean())
#
#     print(pd.Series(model.feature_importances_, index=features).sort_values(ascending=False))
