import pandas as pd
import numpy as np

df = pd.read_csv(
    "C:\\Users\\Manoj\\Downloads\\archive (16)\KaggleV2-May-2016.csv",
    dtype={"PatientId": "string"},
)

df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

df.rename(
    columns={
        "patientid": "patient_id",
        "appointmentid": "appointment_id",
        "scheduledday": "scheduled_day",
        "appointmentday": "appointment_day",
        "noshow": "no_show",
    },
    inplace=True,
)

df["gender"] = df["gender"].str.strip().str.upper()
df["neighbourhood"] = df["neighbourhood"].str.strip().str.title()
df["no_show"] = df["no_show"].str.strip().str.title()

df["scheduled_day"] = pd.to_datetime(df["scheduled_day"], errors="coerce", utc=True)

df["appointment_day"] = pd.to_datetime(df["appointment_day"], errors="coerce", utc=True)

df.drop_duplicates(inplace=True)

df["age"] = pd.to_numeric(df["age"], errors="coerce")
df.loc[~df["age"].between(0, 120), "age"] = np.nan
df["age"] = df["age"].fillna(df["age"].median()).round().astype(int)

df["patient_id"] = df["patient_id"].astype("string")
df["appointment_id"] = pd.to_numeric(df["appointment_id"], errors="coerce").astype(
    "Int64"
)

binary_cols = [
    "scholarship",
    "hipertension",
    "diabetes",
    "alcoholism",
    "handcap",
    "sms_received",
]

for col in binary_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    mode = df[col].mode(dropna=True)
    df[col] = df[col].fillna(mode.iloc[0] if not mode.empty else 0).astype(int)

for col in ["scheduled_day", "appointment_day"]:
    df[col] = df[col].dt.strftime("%d-%m-%Y %H:%M:%S")

df.to_csv("KaggleV2_May_2016_cleaned.csv", index=False)

print("Dataset cleaned successfully!")
print("Shape:", df.shape)
print("\nMissing values:")
print(df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("\nCleaned dataset saved successfully!")
