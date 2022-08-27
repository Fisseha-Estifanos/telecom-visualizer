# import libraries
import pandas as pd
import sqlite3
from sqlite3 import Error

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
    print(conn)
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
        sqlQuery = f"""INSERT INTO {table_name} (created_at, source, original_text, polarity, subjectivity, lang, favorite_count, statuses_count, retweet_count, screen_name, original_author, followers_count, friends_count, possibly_sensitive, hashtags, user_mentions, place, clean_hashtags, clean_mentions)
             VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18])

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

if __name__ == "__main__":
    connection = dbConnect(dbName='telecom.db')
    executeQuery(connection=connection, query='create_user_overview_table.sql')

    df = pd.read_csv('clean_data.csv')
    sample_df = df.copy()
    
    insertToTable(connection=connection, df=sample_df, table_name='userOverview')

    select_query = "select * from userOverview"
    returned_df = dbExecuteFetch(connection, select_query, dbName="telecom.db", rdf=True)
    returned_df.info()
