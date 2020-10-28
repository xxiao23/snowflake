# F1

## Running Presto

1. Install [Java SDK 11](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html) and set JAVA_HOME.
```
export JAVA_HOME=$(/usr/libexec/java_home)
```

2. Download [Presto ver343](https://repo1.maven.org/maven2/io/prestosql/presto-server/343/presto-server-343.tar.gz) and follow [deployment instructions](https://prestosql.io/docs/current/installation/deployment.html).

3. Download [Presto CLI jar](https://repo1.maven.org/maven2/io/prestosql/presto-cli/343/presto-cli-343-executable.jar) and follow [CLI instructions](https://prestosql.io/docs/current/installation/cli.html#) to access Presto via its commandline interface.

## Access Presto via JDBC

1. Download [Presto JDBC jar](https://repo1.maven.org/maven2/io/prestosql/presto-jdbc/344/presto-jdbc-344.jar) and put it in CLASSPATH. Make Sure JDBC jar version matches your presto server version.
```
export CLASSPATH=<path_to_presto_jdbc_jar>/presto-jdbc-344.jar
```

2. Install JayDeBeApi for python to use JDBC `pip install jaydebeapi`.

3. Start a python shell and try the following code. You should be able to see the system tables in Presto.
```python
>>> import jaydebeapi
>>> conn1 = jaydebeapi.connect("com.facebook.presto.jdbc.PrestoDriver",
...                            "jdbc:presto://localhost:8080/system/information_schema", ["root", ""])
>>> curs = conn1.cursor()
>>> curs.execute("select * from tables")
>>> curs.fetchall()
[('system', 'runtime', 'queries', 'BASE TABLE'), ('system', 'runtime', 'transactions', 'BASE TABLE'), ('system', 'information_schema', 'enabled_roles', 'BASE TABLE'), ('system', 'jdbc', 'types', 'BASE TABLE'), ('system', 'jdbc', 'udts', 'BASE TABLE'), ('system', 'metadata', 'column_properties', 'BASE TABLE'), ('system', 'jdbc', 'super_types', 'BASE TABLE'), ('system', 'information_schema', 'views', 'BASE TABLE'), ('system', 'information_schema', 'applicable_roles', 'BASE TABLE'), ('system', 'jdbc', 'procedure_columns', 'BASE TABLE'), ('system', 'information_schema', 'schemata', 'BASE TABLE'), ('system', 'jdbc', 'procedures', 'BASE TABLE'), ('system', 'information_schema', 'columns', 'BASE TABLE'), ('system', 'information_schema', 'table_privileges', 'BASE TABLE'), ('system', 'information_schema', 'roles', 'BASE TABLE'), ('system', 'jdbc', 'pseudo_columns', 'BASE TABLE'), ('system', 'jdbc', 'tables', 'BASE TABLE'), ('system', 'runtime', 'tasks', 'BASE TABLE'), ('system', 'metadata', 'analyze_properties', 'BASE TABLE'), ('system', 'metadata', 'catalogs', 'BASE TABLE'), ('system', 'jdbc', 'attributes', 'BASE TABLE'), ('system', 'jdbc', 'super_tables', 'BASE TABLE'), ('system', 'runtime', 'nodes', 'BASE TABLE'), ('system', 'information_schema', 'tables', 'BASE TABLE'), ('system', 'metadata', 'table_properties', 'BASE TABLE'), ('system', 'jdbc', 'schemas', 'BASE TABLE'), ('system', 'jdbc', 'catalogs', 'BASE TABLE'), ('system', 'jdbc', 'columns', 'BASE TABLE'), ('system', 'jdbc', 'table_types', 'BASE TABLE'), ('system', 'metadata', 'schema_properties', 'BASE TABLE')]
```

## Running Hive 2.3.7 with Hadoop 2.10.1

### Running Hadoop 2.10.1

1. Download [Hadoop 2.10.1](https://www.apache.org/dyn/closer.cgi/hadoop/common/hadoop-2.10.1/hadoop-2.10.1.tar.gz).

2. Start Hadoop in [Pseudo Distributed Mode](https://hadoop.apache.org/docs/r2.10.1/hadoop-project-dist/hadoop-common/SingleCluster.html#Pseudo-Distributed_Operation).

### Troubleshooting

**No datanode**

Find the datanode log (you can access the log from localhost:5007) and check if there is any error in the log.

If you see an error about a temp folder, you can remove the temp folder and restart Hadoop.
```
$ $HADOOP_HOME/bin/stop-dfs.sh
$ $HADOOP_HOME/bin/start-dfs.sh
```

### Running Hive 2.3.7 Metastore Service

1. Download [MySql](https://dev.mysql.com/doc/refman/8.0/en/installing.html) in your environment.

2. Download [Hive 2.3.7](https://mirror.bit.edu.cn/apache/hive/hive-2.3.7/). 

3. Set up MySQL as the metastore DB.
    ```
    $ cd $HIVE_HOME/
    $ mysql
    mysql> CREATE DATABASE metastore;
    mysql> USE metastore;
    mysql> CREATE USER 'hiveuser'@'localhost' IDENTIFIED BY 'password';
    mysql> GRANT GRANT ALL PRIVILEGES ON metastore.* TO 'hiveuser'@'localhost'; 
    mysql> FLUSH PRIVILEGES;
    ```

4. In addition, you must use below HDFS commands to create /tmp and /user/hive/warehouse (aka hive.metastore.warehouse.dir) and set them chmod g+w before you can create a table in Hive.

    ```
    $HADOOP_HOME/bin/hdfs dfs -mkdir       /tmp
    $HADOOP_HOME/bin/hdfs dfs -mkdir -p    /user/hive/warehouse
    $HADOOP_HOME/bin/hdfs dfs -chmod g+w   /tmp
    $HADOOP_HOME/bin/hdfs dfs -chmod g+w   /user/hive/warehouse
    ```

5. Copy hive-default-xml to hive-site.xml
    ```
    $ cd $HIVE_HOME/conf
    $ cp hive-default.xml.template hive-site.xml
    ```

6. Edit following lines in hive-site.xml
    ```
    <property>
        <name>javax.jdo.option.ConnectionURL</name>
        <value>jdbc:mysql://localhost/metastore?useUnicode=true&amp;useJDBCCompliantTimezoneShift=true&amp;useLegacyDatetimeCode=false&amp;serverTimezone=UTC</value>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionDriverName</name>
        <value>com.mysql.jdbc.Driver</value>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionUserName</name>
        <value>hiveuser</value>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionPassword</name>
        <value>password</value>
    </property>
    <property>
        <name>datanucleus.fixedDatastore</name>
        <value>false</value>
    </property>
    <property>
        <name>hive.exec.local.scratchdir</name>
        <value>/tmp/hive</value>
        <description>Local scratch space for Hive jobs</description>
    </property>
    <property>
        <name>hive.downloaded.resources.dir</name>
        <value>/tmp/hive</value>
        <description>Temporary local directory for added resources in the remote file system.</description>
    </property>
    <property>
        <name>hive.querylog.location</name>
        <value>/tmp/hive</value>
        <description>Location of Hive run time structured log file</description>
    </property>
    ```

7. Download JDBC
    Go to mysql page and download the latest jdbc (sign up is required) http://dev.mysql.com/downloads/connector/j/
    ```
    $ tar zxvf mysql-connector-java-<version>.tar.gz
    $ sudo cp mysql-connector-java-<version>/mysql-connector-java-<version>-bin.jar $HIVE_HOME/lib/
    ```

7. Init Metastore Schema
    ```
    $ $HIVE_HOME/bin/schematool -dbType mysql -initSchema
    ```

8. Run Hive
    ```
    $ cd $HIVE_HOME
    $ bin/hive
    ```

9. Run Hive Metastore Service
    ```
    $ cd $HIVE_HOME
    $ bin/hive --service metastore
    ```

## Running Presto with Hive Connector

1. Configuration

    Create etc/catalog/hive.properties with the following contents to mount the hive-hadoop2 connector as the hive catalog, with the correct host and port for your Hive metastore Thrift service:
    ```
    connector.name=hive-hadoop2
    hive.metastore.uri=thrift://localhost:9083
    ```

2. HDFS Username and Permissions

    Override this username by setting the HADOOP_USER_NAME system property in the Presto JVM Config, replacing hdfs_user with the appropriate username:
    ```
    -DHADOOP_USER_NAME=hiveuser
    ```

3. Create a table in Hive.
    ```
    CREATE TABLE pokes (foo INT, bar STRING);
    ```

4. Start Presto.

5. Connect to Presto/Hive.
    ```
    ./presto --server localhost:8080 --catalog hive --schema default
    presto>show tables;
    ```
    You should be able to see `pokes` table that you created in Hive.

## Using Hive Connect with AWS S3

1. Configuration

    Add AWS S3 credentials.
    ```
    hive.s3.aws-access-key=<aws_access_key>
    hive.s3.aws-secret-key=<aws_secret_key>
    ```