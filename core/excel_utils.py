import pandas as pd

def read_users(path, sheet):
    df = pd.read_excel(path, sheet_name=sheet)
    required = ['Name', 'Email', 'Password', 'ConfirmPassword']
    for c in required:
        if c not in df.columns:
            raise ValueError(f"Missing column in Excel: {c}")
    return df.to_dict(orient='records')

def write_results(df, path='referral_results.xlsx'):
    df.to_excel(path, index=False)
