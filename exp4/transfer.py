import pandas as pd
import pypyodbc as odbc

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = r'Ashish\SQLEXPRESS'
DATABASE_NAME = 'ashish'
TABLE_NAME = 'Parquet'

connection_string = 'DRIVER={%s};SERVER=%s;DATABASE=%s;Trusted_Connection=yes' % (DRIVER_NAME, SERVER_NAME, DATABASE_NAME)

try:
    # Read the Parquet file
    ParquetFile = pd.read_parquet('cars.parquet')
    
    # Extract column names and data types
    column_names = ParquetFile.columns.tolist()
    column_data_types = ParquetFile.dtypes
    
    # Construct SQL query to create table
    create_table_query = f"CREATE TABLE {TABLE_NAME} (\n"
    for column_name, data_type in zip(column_names, column_data_types):
        sql_data_type = 'VARCHAR(MAX)' if data_type == 'object' else 'VARCHAR(MAX)'  # Change to appropriate SQL data type for non-object columns
        create_table_query += f"{column_name} {sql_data_type},\n"
    create_table_query = create_table_query.rstrip(',\n')  # Remove trailing comma and newline
    create_table_query += "\n)"
    # print(create_table_query)
    
    # Connect to the database and execute the query to create table
    connection = odbc.connect(connection_string)
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    
    # Insert data into the table
    for index, row in ParquetFile.iterrows():
        values = tuple(row)
        insert_query = f"INSERT INTO {TABLE_NAME} ({', '.join(column_names)}) VALUES ({', '.join(['?'] * len(column_names))})"
        cursor.execute(insert_query, values)
    
    connection.commit()
    
    print("Table created and data inserted successfully.")
    
except Exception as e:
    print("Error:", e)