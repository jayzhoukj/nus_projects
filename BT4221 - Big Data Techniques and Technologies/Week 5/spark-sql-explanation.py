
# We are importing the Sparksessin object and the Row object. The SparkSession object is basically Spark's way of creating a context to work with SparkSQL.
from pyspark.sql import SparkSession
from pyspark.sql import Row

# We are also import collections here.
import collections

# We are creating SparkSession object. However, we used to create sparkContext object before. So what we are doing here is creating someting called spark that is going to be a SparkSession object. We will use a builder method on it, then we will just combine these different parameters to actually get a session that we can work with. This will give us not only SparkContext, but also a SQL context that we can use to issue SQL queries on.
# Note, the config section is only for Window. It is kind of a workaround, a bug in Spark 2.0. If you are not on Windows, leave that part as is and make sure you have a temp folder in your C: drive; otherwise, point it to someplace else.
# We are going to give appName a name SparkSQL and then call getOrCreate to create it. This gives back a SparkSession object that we can start using.

# For windows students
spark = SparkSession.builder.config("spark.sql.warehouse.dir", "file:///C:/temp").appName("SparkSQL").getOrCreate()

# For non-windows students
spark = SparkSession.builder.appName("SparkSQL").getOrCreate()


# What we are going to do is take our fake social network data and use SQL queries to analyze it instead of doing RDD operationss. Unfortunately, this data is not structured to begin with. It is just a CSV file, a bunch of text as far as we are concerned. So, before we can import the data into a structured DataFrame object, we need to provide some structure to it.
# Just like we would normally open up the text file adn give it to a mapper to convert it into a Row object.
# This is basically converting an RDD that is splits comma-separated values into a DataFrame. Please remember that a DataFrame in Python is really just an RDD of Row object.

def mapper(line):
    fields = line.split(',')
    return Row(ID=int(fields[0]), name=str(fields[1].encode("utf-8")), age=int(fields[2]), numFriends=int(fields[3]))


# We call sparkContext o nthe SparkSession object we created. This gives us the same kind of sparkContext we saw previously. From there, we cna just call textFile with fakefriends.csv.

lines = spark.sparkContext.textFile("fakefriends.csv")

# No that we have sparkContext, we can pass it to our mapper function. The mapper function splits up each line by commas and then creates Row objects, and as you can see, we're giving some structure to these objects. We are going to have an ID column that would consist of customer ID, a name column for a string name, an age column that would be integer-based, and a numFriends colimn that would be integer-based as well. Thus, this mapper basically provides the structure and specifically types information back to our RDD.
people = lines.map(mapper)

# From now on, you can think of people as almost a DataFrame. We need to call spark.createDataFrame to officially make it a DataFrame and take the RDD of row objects and treat it as a DataFrame.

# Infer the schema, and register the DataFrame as a table. At the end of the line, we will cache spark.createDataFrame becuase we are going to do more than one thing to it.
schemaPeople = spark.createDataFrame(people).cache()

# We are going to temporary SQL table in memory, called people, that we can issue queries on. schemaPeople is now a Dataframe, it will look at those rows and the names of those rows and subsequently create columns.
schemaPeople.createOrReplaceTempView("people")

# SQL can be run over DataFrames that have been registered as a table. Remember that spark is the name of SparkSession. We write out our SQL query, just like it were a SQL database. Because we defined our Row object with a parameter of age, it knows that the age corresponds to the third column of the dataFrame.
teenagers = spark.sql("SELECT * FROM people WHERE age >= 13 AND age <= 19")

# The results of SQL queries are RDDs and support all the normal RDD operations. Collect will print out 20 results.
for teen in teenagers.collect():
  print(teen)

# We can also use functions instead of SQL queries. We are calling groupBy, using the age column, and then doing a count. This is exactly like issuing a SQL query that is gropued by age and counting and then ordering the results by age and showing them. The following line is that it groups together all the people of a given age and counts them up-at this point, we have a dataFrame of ages and how many people of that age occur in the DataFrame.

# In the following code, we have done what would otherwise have been a more complicated and convoluted implementaotin using stright up RDDs. We do not need to create (key,value)RDDs where the value is 1, and then reduce tem together to count them up.
schemaPeople.groupBy("age").count().orderBy("age").show()

spark.stop()
