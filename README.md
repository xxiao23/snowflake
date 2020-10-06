# Snowflake

## Running Presto

0. Install [Presto](https://prestodb.io/docs/current/installation.html).
1. Install [Java SDK](https://www.oracle.com/java/technologies/javase-jdk15-downloads.html).
```
export JAVA_HOME=$(/usr/libexec/java_home)
```
2. Download [Presto JDBC jar](https://repo1.maven.org/maven2/com/facebook/presto/presto-jdbc/0.241/presto-jdbc-0.241.jar) and put it in CLASSPATH. Make Sure JDBC jar version matches your presto server version.
```
export CLASSPATH=/Users/mrxiangxiao/Downloads/presto-jdbc-0.235.1.jar
```
3. Install JayDeBeApi for python to use JDBC `pip install jaydebeapi`.
4. Start a python shell and try the following code. You should be able to see the system tables in Presto.
```python
>>> import jaydebeapi
>>> conn1 = jaydebeapi.connect("com.facebook.presto.jdbc.PrestoDriver",
...                            "jdbc:presto://localhost:8080/system/information_schema", ["root", ""])
>>> curs = conn1.cursor()
>>> curs.execute("select * from tables")
>>> curs.fetchall()
[('system', 'runtime', 'queries', 'BASE TABLE'), ('system', 'runtime', 'transactions', 'BASE TABLE'), ('system', 'information_schema', 'enabled_roles', 'BASE TABLE'), ('system', 'jdbc', 'types', 'BASE TABLE'), ('system', 'jdbc', 'udts', 'BASE TABLE'), ('system', 'metadata', 'column_properties', 'BASE TABLE'), ('system', 'jdbc', 'super_types', 'BASE TABLE'), ('system', 'information_schema', 'views', 'BASE TABLE'), ('system', 'information_schema', 'applicable_roles', 'BASE TABLE'), ('system', 'jdbc', 'procedure_columns', 'BASE TABLE'), ('system', 'information_schema', 'schemata', 'BASE TABLE'), ('system', 'jdbc', 'procedures', 'BASE TABLE'), ('system', 'information_schema', 'columns', 'BASE TABLE'), ('system', 'information_schema', 'table_privileges', 'BASE TABLE'), ('system', 'information_schema', 'roles', 'BASE TABLE'), ('system', 'jdbc', 'pseudo_columns', 'BASE TABLE'), ('system', 'jdbc', 'tables', 'BASE TABLE'), ('system', 'runtime', 'tasks', 'BASE TABLE'), ('system', 'metadata', 'analyze_properties', 'BASE TABLE'), ('system', 'metadata', 'catalogs', 'BASE TABLE'), ('system', 'jdbc', 'attributes', 'BASE TABLE'), ('system', 'jdbc', 'super_tables', 'BASE TABLE'), ('system', 'runtime', 'nodes', 'BASE TABLE'), ('system', 'information_schema', 'tables', 'BASE TABLE'), ('system', 'metadata', 'table_properties', 'BASE TABLE'), ('system', 'jdbc', 'schemas', 'BASE TABLE'), ('system', 'jdbc', 'catalogs', 'BASE TABLE'), ('system', 'jdbc', 'columns', 'BASE TABLE'), ('system', 'jdbc', 'table_types', 'BASE TABLE'), ('system', 'metadata', 'schema_properties', 'BASE TABLE')]
```
5. Load TPCH data by creating [a TPCH connect](https://prestodb.io/docs/current/connector/tpch.html).
