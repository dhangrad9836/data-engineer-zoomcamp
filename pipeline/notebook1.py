#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd


# In[8]:


#we split up the url in two parts the prefix and url to make and entire url 
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
url = f'{prefix}/yellow_tripdata_2021-01.csv.gz'
url


# In[36]:


df = pd.read_csv(url)


# In[10]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    url,
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)


# In[35]:


df.head()


# In[34]:


df['VendorID']


# In[2]:


get_ipython().system('uv add sqlalchemy')


# In[33]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[4]:


get_ipython().system('uv add psycopg2-binary')


# In[5]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[14]:


df.head(0)


# In[15]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[32]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[17]:


len(df)


# In[18]:


len


# In[38]:


df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)


# In[39]:


print(df_iter)


# In[40]:


df = next(df_iter)


# In[28]:


df


# In[41]:


print(df)


# In[29]:


get_ipython().system('uv add tqdm')


# In[30]:


from tqdm.auto import tqdm


# In[42]:


for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')



# In[ ]:




