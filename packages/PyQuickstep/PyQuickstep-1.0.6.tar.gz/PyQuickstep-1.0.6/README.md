# PyQuickstep  
The Quickstep Python API was designed and developed based on the guidelines from [Python Database API Specification](https://www.python.org/dev/peps/pep-0249/). The API is used as a access layer for [Quickstep DBMS](https://github.com/apache/incubator-quickstep). The API contains the following modules:

* Connection – An instance of connection supports two methods.
    *	close() – closes the connection between API and Quickstep instance.
    *	cursor() – Gives a cursor instance to interact with Quickstep database instance.
* Cursor – An instance of cursor is used to manage the context of operations to the Quickstep database.
    *	close() – Closes the cursor and will be not usable after this.
    *	execute() – Executes the given query and returns result after formatting to tuples.
    *	fetchone() – fetches one row and moves the cursor to next row.
    *   fetchmany() – fetches mentioned number of rows and moves the cursor to next    row if available.
    *	fetchall() – fetches all the rows and moves the cursor to the end.
* Error – Defines the different types of errors and warnings that API can produce.
* QuickstepResult – Parses the query result into tuples.
* GPRC files – Generated files to establish connection with the Quickstep database.

## Installation:  

PyQuickstep is uploaded to PyPI.
It can be installed with the following command:

`$python2 -m pip install pyquickstep`


## Example:  

The following example makes use of simple table. Create the table in Quickstep database.

```
CREATE TABLE Weather (cid INTEGER, recordDate DATE, highTemperature FLOAT, lowTemperature FLOAT);  
INSERT INTO Weather VALUES (1, '2015-11-1', 50, 30);     
INSERT INTO Weather VALUES (1, '2015-11-2', 51, 32);    
INSERT INTO Weather VALUES (2, '2015-11-1', 60, 50);
```  

```
import pyquickstep  
conn = pyquickstep.Connect('localhost', '3000')  
cursor = conn.cursor()  
result = cursor.execute("select * from weather")  
print cursor.fetchone()
print cursor.fetchmany()
print cursor.fetchall()
```

This example will print:  
```
('1', '2015-11-01', '50', '30')  
(('1', '2015-11-02', '51', '32'),)  
(('2', '2015-11-01', '60', '50'),)  
```

## License  

PyQuickstep is licensed under GNU GPLv3. Please see LICENSE
