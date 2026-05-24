import pandas as pd
import streamlit as st
import boto3
import os

def get_s3_client():
    env = os.getenv("APP_ENV", "local")

    if env == "local":
        from dotenv import load_dotenv
        load_dotenv()

        return boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_DEFAULT_REGION"),
        )

    # Production: boto3 automatically picks up the ECS Task Role
    # via the container's metadata credential endpoint — no config needed
    return boto3.client("s3")

def _parse_image_list(imgStringList):
    if not isinstance(imgStringList, str):
        return imgStringList
    return [url.strip() for url in imgStringList.strip('[]').split(', ') if url.strip()]

@st.cache_data
def loadData(queryName):
    try:
        s3 = get_s3_client()
        bucket, prefix = 'hajjpackagedata', f'athena-results/{queryName}/'
        
        objects = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        csv_files = sorted(
            [o for o in objects.get('Contents', []) if o['Key'].endswith('.csv')],
            key=lambda o: o['LastModified']
        )
        
        latest = csv_files[-1]['Key']
        df = pd.read_csv(s3.get_object(Bucket=bucket, Key=latest)['Body'])
        for col in ('makkah_images', 'madinah_images'):
          df[col] = df[col].apply(_parse_image_list)
        # df.reset_index()
        return df, None
    except Exception as e:
        return None, e

if __name__ == "__main__":
  df, err = loadData('allData')
  if err is None:
    print(df.shape)
    # print(df.head())
    print(df.columns.values)
  else:
     print(str(err))
