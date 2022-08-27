# import libraries
import pandas as pd
import sqlite3
from sqlite3 import Error
from sqlalchemy import create_engine


def dbConnect(dbName=None):
    """
    A data base connection creator method.

    Parameters
    ----------
    dbName :
        Default value = None
        string : the database name

    Returns :
        sqlite.connection : the database connection
    -------
    """
    conn = sqlite3.connect(dbName)
    print(f'connection created: {conn}')
    print(f'database name: {dbName}')
    return conn

def executeQuery(connection: sqlite3.Connection, query:str) -> None:
    """
    A data base query executor method, based on a given connection string and a query string

    Parameters
    ----------
    connection :
        sqlite3.Connection : the database connection
    query :
        string : the query string
    Returns :
    -------
    return : nothing
    """

    cursor = connection.cursor()
    print(f'query string: {query}')
    fd = open(query, 'r')
    sql_query = fd.read()
    fd.close()

    try:
        cursor.execute(sql_query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def insertToTable(connection: sqlite3.Connection, df: pd.DataFrame, table_name: str) -> None:
    """
    A method to insert dataframe data into a data base

    Parameters
    ----------
    connection :
        sqlite3.Connection : the database connection
    df :
        pd.DataFrame : the dataframe
    table_name :
        str : the tablename
    Returns :
        nothing
    -------
    """
    for _, row in df.iterrows():
        sqlQuery = f"""INSERT INTO {table_name} ('Bearer Id', Start, End, Dur, IMSI, 'MSISDN/Number', IMEI, 'Last Location Name', 'Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)', 'TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)', 'HTTP DL (Bytes)', 'HTTP UL (Bytes)', 'Activity Duration DL (ms)', 'Activity Duration UL (ms)', 'Handset Manufacturer', 'Handset Type')
             VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19])

        try:
            cur = connection.cursor()
            # Execute the SQL command
            cur.execute(sqlQuery, data)
            # Commit your changes in the database
            connection.commit()
            print(f"{_}: Data Inserted Successfully")
            cur.close()
        except Exception as e:
            connection.rollback()
            print("Error: ", e)

def dbExecuteFetch(connection:sqlite3.Connection, selection_query : str, dbName : str, rdf=True, many = False) -> pd.DataFrame:
    """
    A method to execute a fetch query based on a given selection query 

    Parameters
    ----------
    *args :

    many :
         (Default value = False)
    tablename :
         (Default value = '')
    rdf :
         (Default value = True)
    **kwargs :

    Returns
    -------
    Dataframe:
        pandas dataframe
    """   
    
    cursor1 = connection.cursor()
    result = None
    try:
        cursor1.execute(selection_query)
        result = cursor1.fetchall()
    except Error as e:
        print(f"The error '{e}' occurred")

    #print(result[0], end="\n\n")
    # get column names
    field_names = [i[0] for i in cursor1.description]

    cursor1.close()
    connection.close()

    # return result
    if rdf:
        return pd.DataFrame(result, columns=field_names)
    else:
        return result

def createEngine():
    # create an engine to connect to our data base server
    engine = create_engine('mysql+pymysql://root:@localhost/telecom')
    return engine 

def addToTable(engine):
    # writing to the data base server
    try:
        print('reading csv as a pandas dataframe...')
        user_overview_df = pd.read_csv('Week1_challenge_data_source_filled.csv.bz2')
        
        print('writing to the database...')
        frame = user_overview_df.sample(frac=0.01).to_sql("UserOverview", con=engine, if_exists='replace')

        print('data successfully saved to database')
    except Exception as e:
        print("Error writing to database: ", e)

if __name__ == "__main__":
    #connection = dbConnect(dbName='telecom.db')
    #executeQuery(connection=connection, query='create_user_overview_table.sql')

    #df = pd.read_csv('Week1_challenge_data_source_filled.csv.bz2')
    #sample_df = df.copy()
    
    #insertToTable(connection=connection, df=sample_df.iloc[:1000], table_name='UserOverview')

    #select_query = "select * from UserOverview"
    #returned_df = dbExecuteFetch(connection, select_query, dbName="telecom.db", rdf=True)
    #returned_df.info()

    # -------------- #

    # get database engine
    print('generating database engine...')
    engine = createEngine()
    addToTable(engine)

    # reading data from the data base server
    pd.read_sql("select * from telecom.UserOverview", engine)

    # -------------- #