import pandas as pd
import streamlit as st
import ast 
from hajj_or_umrah_enum import HajjOrUmrahEnum

# import boto3
# import os

# def get_s3_client():
#     env = os.getenv("APP_ENV", "local")

#     if env == "local":
#         from dotenv import load_dotenv
#         load_dotenv()

#         return boto3.client(
#             "s3",
#             aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#             aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
#             region_name=os.getenv("AWS_DEFAULT_REGION"),
#         )

#     # Production: boto3 automatically picks up the ECS Task Role
#     # via the container's metadata credential endpoint — no config needed
#     return boto3.client("s3")

# @st.cache_data
# def loadData(queryName):
#     try:
#         s3 = get_s3_client()
#         bucket, prefix = 'hajjpackagedata', f'athena-results/{queryName}/'

#         objects = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
#         csv_files = sorted(
#             [o for o in objects.get('Contents', []) if o['Key'].endswith('.csv')],
#             key=lambda o: o['LastModified']
#         )

#         latest = csv_files[-1]['Key']
#         df = pd.read_csv(s3.get_object(Bucket=bucket, Key=latest)['Body'])
#         for col in ('makkah_images', 'madinah_images'):
#           df[col] = df[col].apply(_parse_image_list)
#         # df.reset_index()
#         return df, None
#     except Exception as e:
#         return None, e
    

HAJJ_DATA_URL = "https://hajjpackagedata.s3.eu-north-1.amazonaws.com/athena-results/allData/092aac6e-569a-48fd-9eb6-6ec98ffb999d.csv"
UMRAH_DATA_URL = "https://umrahpackagedata.s3.eu-north-1.amazonaws.com/athena-results/allData/a6e5844c-b699-4cdc-a150-e1ce50804f68.csv"

URL_MAP = {HajjOrUmrahEnum.HAJJ: HAJJ_DATA_URL, HajjOrUmrahEnum.UMRAH: UMRAH_DATA_URL}

def _parse_image_list(raw):
    """Parse a stored image-list field (e.g. stringified list) into a list of URLs."""
    if isinstance(raw, list):
        return raw
    if pd.isna(raw) or not raw:
        return []
    try:
        parsed = ast.literal_eval(raw)
        return parsed if isinstance(parsed, list) else []
    except (ValueError, SyntaxError, TypeError):
        return []


def _load_csv(url):
  df = pd.read_csv(url)
  for col in ('makkah_images', 'madinah_images'):
    if col in df.columns:
      df[col] = df[col].apply(_parse_image_list)
  
  return df

@st.cache_data
def load_data(hajj_or_umrah: HajjOrUmrahEnum) -> pd.DataFrame:
  return _load_csv(URL_MAP[hajj_or_umrah])

@st.cache_data
def load_company_df(company_name: str, pilgrimage_type: HajjOrUmrahEnum) -> pd.DataFrame:
    """Rows for a single company within a pilgrimage type."""
    df = load_data(pilgrimage_type)
    return df[df['company'] == company_name].reset_index(drop=True)

if __name__ == "__main__":
  for x in [HajjOrUmrahEnum.HAJJ, HajjOrUmrahEnum.UMRAH]:
      try:
          df = load_data(x)
          print(x.label, df.shape)
          print(df.columns.values)
      except Exception as e:
         print(x.label, str(e))
