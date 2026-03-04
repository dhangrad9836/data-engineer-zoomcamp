#!/usr/bin/env python
# coding: utf-8

"""
NYC Taxi Data Ingestion Script
Loads CSV data into PostgreSQL database in chunks
"""

import click, os
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


# Data types for NYC taxi dataset
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

# Columns to parse as datetime
parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


def ingest_data(
        url: str,
        engine,
        target_table: str,
        chunksize: int = 100000,
) -> None:
    """
    Download CSV/Parquet data and ingest into PostgreSQL

    Args:
        url: URL or path to CSV/Parquet file
        engine: SQLAlchemy database engine
        target_table: Name of table to create/replace
        chunksize: Number of rows per chunk (for CSV only)
    """
    ext = os.path.splitext(url)[1]
    
    if ext == ".parquet":
        # Parquet: load all at once (already compressed/efficient)
        print("Loading parquet file...")
        df = pd.read_parquet(url)
        
        # Create table and insert all data
        df.to_sql(
            name=target_table,
            con=engine,
            if_exists="replace",
            index=False
        )
        
        print(f"✅ Table '{target_table}' created")
        print(f"✅ Inserted {len(df):,} rows")
        print(f"🎉 Done ingesting to '{target_table}'!")
        
    else:
        # CSV: load in chunks
        try:
            # Try with custom dtypes for taxi data
            df_iter = pd.read_csv(
                url,
                dtype=dtype,
                parse_dates=parse_dates,
                iterator=True,
                chunksize=chunksize
            )
        except Exception:
            # Fallback: load without dtypes (for zones, other data)
            df_iter = pd.read_csv(
                url,
                iterator=True,
                chunksize=chunksize
            )

        # Get first chunk
        first_chunk = next(df_iter)

        # Create table schema (no data)
        first_chunk.head(0).to_sql(
            name=target_table,
            con=engine,
            if_exists="replace"
        )
        print(f"✅ Table '{target_table}' created")

        # Insert first chunk
        first_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append"
        )
        print(f"✅ Inserted first chunk: {len(first_chunk):,} rows")

        # Insert remaining chunks with progress bar
        for df_chunk in tqdm(df_iter, desc="Loading chunks"):
            df_chunk.to_sql(
                name=target_table,
                con=engine,
                if_exists="append"
            )

        print(f"🎉 Done ingesting to '{target_table}'!")


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--chunksize', default=100000, type=int, help='Chunk size')
@click.option('--target-table', default='taxi_zone_lookup', help='Target table name')
@click.option('--file', default=None, help='Local file path instead of URL')

def main(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, chunksize, target_table, file):
    """Ingest NYC Taxi CSV data into PostgreSQL database"""

    # Build database connection
    engine = create_engine(
        f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    )

    # Build data URL
    # url_prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
    url_prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
    #url = f'{url_prefix}/yellow_tripdata_{year:04d}-{month:02d}.csv.gz'
    #url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
    
    # Decide whether to use local file or remote URL 
    if file: 
        url = file
        is_local = True 
    else: 
        url = f"{url_prefix}/yellow_tripdata_{year:04d}-{month:02d}.csv.gz"


    print(f"📥 Downloading: {url}")
    print(f"📊 Target table: {target_table}")
    print(f"🖥️  Database: {pg_host}:{pg_port}/{pg_db}")

    # Run ingestion
    ingest_data(
        url=url,
        engine=engine,
        target_table=target_table,
        chunksize=chunksize
    )


if __name__ == '__main__':
    main()