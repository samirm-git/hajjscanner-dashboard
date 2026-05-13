import pandas as pd
import streamlit as st
import boto3

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


@st.cache_data
def loadData(queryName):
    try:
        s3 = boto3.client('s3')
        bucket, prefix = 'hajjpackagedata', f'athena-results/{queryName}/'
        
        objects = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        csv_files = sorted(
            [o for o in objects.get('Contents', []) if o['Key'].endswith('.csv')],
            key=lambda o: o['LastModified']
        )
        
        latest = csv_files[-1]['Key']
        df = pd.read_csv(s3.get_object(Bucket=bucket, Key=latest)['Body'])
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
