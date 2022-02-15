# taskeasy-test
I present the solution for the challenge provided.
## Exercise #1
For this exercise I've proposed a very basic pipeline to populate the tables of a **SQLite** Database from an Excel file. Please check the answers following the next links:
* [Schema of DB tables](Schemas.sql)
* [Ingestion pipeline](exercise_001.py)
* [SQL Solutions](exercise_001.ipynb)

## Exercise #2
**Setup**:  
In this scenario imagine we have a single table with 500k records, and the table having the columns of First Name, Last Name and Age with no indexing on any columns.  
**Challenge**:  
If we index the Age column of this table, what effect does it have on the table's performance? 

---

**Solution**:  
In this case since the year field is a **non-unique** value the effect of the index would be to make faster data retrieval clustered by **age** this means that if I run a query like:
~~~~sql
SELECT
    COUNT(*) AS persons_under_50
FROM
    table_A
WHERE
    age <= 50;
~~~~ 
It's going to run faster if the table is indexed by age because underneath there will be a lookup table that points exactly where the age is greater than 50. Another advantage of the indexing is that the *update* statement (only when updating a few rows) is going to run faster since we have direct access to rows, apart from that there exists few disadvantages with indexing one is that the lookup table needs additional disk space, the writing operations on the table are going to be slow because at the time of **inserting** or **deleting** the index lookup table has to update all the modified indexes as well.  
**Resources**:  
* https://www.tutorialspoint.com/sqlite/sqlite_indexes.htm
* https://stackoverflow.com/questions/1108/how-does-database-indexing-work

**Experience**:  
On my experience I used to apply column indexing on databases with unique id's that handles a lot of retreival requests like from API's, because the indexing will optimize the searching methods for a better retreival query performance.

---

## Exercise #3
**Setup**:  
In this scenario imagine we have 4 tables we need to pull data from. We often pull data from these same 4 tables, the same way, and use that data for other reporting or to display somewhere.  
**Challenge**:  
Since this data is often pulled the same way and done so frequently, would you move this query to a *View* or a *Stored procedure*. Please explain why.  

----

**Solution**:  
For this problem I propose to use a *View* approach, once the *View* is defined everytime we query that *View* it would make the update of the original query retreived data.  
**Experience**:  
On my current work we used to create views for specific reports that takes information of many tables in order to get the updated info at each call and we use SP's when the solution involves to process or call complex functions to transform the data.       
 
----

## Exercise #4
**Setup**:  
In this scenario there is a table that is replicated from a different datasource. We'll call this table **A**. Table **A** needs to be updated with the source data at least every 15 minutes. The changes that may occur to table **A** are, added rows, updated rows and deleted rows.  
**Challenge**:  
In general terms describe how to create a script (suggested python / SQL) that would replicate data from the source data to table **A**.  

---

**Solution**:  
For this challenge my proposed architecture is shown in the image below:

![Replicate](Replicate.jpg)  

1. Trigger / Scheduler: This part is needed for job orchestration, I've experience using *cron* and some hands on *Apache airflow*.
2. Source: There are a lot of possibilities here, but for this exercise I assume the data source as a relational database.
3. Worker: Is the principal executor of the job, is trigger by the scheduler to execute a routine written in python and sql.
4. Destination: Where the processed data is going to be stored? For this exercise I assume that is another relational database. 

Now that the architecture is clear I've worked on a basic script to create a data replication between 2 databases using python and SQL instructions. Please check the script here: [exercise_004.py](exercise_004.py).  
~~~~python
# Create engine for database A and B
try:
    engine_a = create_engine('sqlite:///test.db', echo=False)
    engine_b = create_engine('postgresql://test:test@localhost/test')
    print('Engines created succesfully')
    
except Exception as e:
    print(f'Error trying to create engines : {e}')
        

def replicate(table_name):
    # Replication function
    try:
        df_origin = pd.read_sql(f'SELECT * FROM {table_name}', con=engine_a)
        df_origin.to_sql(table_name, if_exists='Replace', con=engine_b)
        print('Replication successful!')
    except Exception as e:
        print(f'Error during replication: {e}')
~~~~
Using the *create_engine* method from sqlalchemy I could establish a database connection to **source** and **destination**. Then using pandas *sql* functions I can read data from **source** database using its specific engine and then move that information to the **destination** database.  
**Note**: *This code could be optimized for large datasets using **iter** functions on dataframes by only allocating in memory XXXXXX rows of the query response and iterating on chuncks to write on the destination database* 

The code below shows a better implementation of the replicate function to allow large dataset without running out of memory.
~~~~python
def replicate_optimized(table_name):
    df_iter = pd.read_sql(f'SELECT * FROM {table_name}', con=engine_a iterator=True, chunksize=100000)
    df = next(df_iter)
    df.to_sql(table_name, con=engine_b, if_exists='replace')

    while True:
        try:
            df = next(df_iter)
        except StopIteration:
            print('Replicate task finished')
            break
        df.to_sql(table_name, con=engine_b, if_exists='replace')
~~~~
