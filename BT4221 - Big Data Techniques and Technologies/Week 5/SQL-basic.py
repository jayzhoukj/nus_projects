

# Basic
import findspark
findspark.init()
from pyspark import SparkConf, SparkContext
from decimal import Decimal
conf = SparkConf().setMaster("local").setAppName("Bankaccount-SQL")
sc = SparkContext(conf = conf)

# Creation of the list from where the RDD is going to be created
acTransList = ["SB10001,1000", "SB10002,1200", "SB10003,8000", "SB10004,400", "SB10005,300", "SB10006,10000", "SB10007,500", "SB10008,56", "SB10009,30","SB10010,7000", "CR10001,7000", "SB10002,-10"]
# Create the RDD
acTransRDD = sc.parallelize(acTransList)
# Collect the values from the RDDs to the driver program
acTransRDD.collect()

# Apply filter and create another RDD of good transaction records
goodTransRecords = acTransRDD.filter(lambda trans: Decimal(trans.split(",")[1]) > 0).filter(lambda trans: (trans.split(",")[0]).startswith('SB') == True)

# Collect the values from the RDDs to the driver program
goodTransRecords.collect()

# Apply filter and create another RDD of high value transaction records
highValueTransRecords = goodTransRecords.filter(lambda trans: Decimal(trans.split(",")[1]) > 1000)

# Collect the values from the RDDs to the driver program
highValueTransRecords.collect()

# The function that identifies the bad amounts
badAmountLambda = lambda trans: Decimal(trans.split(",")[1]) <= 0

# Collect the values from the RDDs to the driver program
badAccountRecords.collect()


# The function that identifies bad accounts
badAcNoLambda = lambda trans: (trans.split(",")[0]).startswith('SB') == False
# Apply filter and create another RDD of bad amount records
badAmountRecords = acTransRDD.filter(badAmountLambda)
# Collect the values from the RDDs to the driver program
badAmountRecords.collect()

# Apply filter and create another RDD of bad account records
badAccountRecords = acTransRDD.filter(badAcNoLambda)
# Do the union of two RDDs and create another RDD
badTransRecords  = badAmountRecords.union(badAccountRecords)
# Collect the values from the RDDs to the driver program
badTransRecords.collect()


# The function that calculates the sum
sumAmount = goodTransRecords.map(lambda trans: Decimal(trans.split(",")[1])).reduce(lambda a,b : a+b)
sumAmount

# The function that calculates the maximum
maxAmount = goodTransRecords.map(lambda trans: Decimal(trans.split(",")[1])).reduce(lambda a,b : a if a > b else b)
maxAmount

# The function that calculates the minimum
minAmount = goodTransRecords.map(lambda trans: Decimal(trans.split(",")[1])).reduce(lambda a,b : a if a < b else b)
minAmount


# Combine all the elements
combineAllElements = acTransRDD.flatMap(lambda trans: trans.split(","))
combineAllElements.collect()

# Find the good account numbers
allGoodAccountNos = combineAllElements.filter(lambda trans: trans.startswith('SB') == True)
allGoodAccountNos.distinct().collect()


# Create the RDD
acTransRDD = sc.parallelize(acTransList)
# Create the RDD containing key value pairs by doing mapping operation
acKeyVal = acTransRDD.map(lambda trans: (trans.split(",")[0],Decimal(trans.split(",")[1])))
# Create the RDD by reducing key value pairs by doing applying sum operation to the values
accSummary = acKeyVal.reduceByKey(lambda a,b : a+b).sortByKey()

# Collect the values from the RDDs to the driver program
accSummary.collect()



# Creation of the list from where the RDD is going to be created
acMasterList = ["SB10001,Roger,Federer", "SB10002,Pete,Sampras", "SB10003,Rafel,Nadal", "SB10004,Boris,Becker", "SB10005,Ivan,Lendl"]
# Creation of the list from where the RDD is going to be created
acBalList = ["SB10001,50000", "SB10002,12000", "SB10003,3000", "SB10004,8500", "SB10005,5000"]
# Create the RDD
acMasterRDD = sc.parallelize(acMasterList)
# Collect the values to the driver program
acMasterRDD.collect()

# Create the RDD
acBalRDD = sc.parallelize(acBalList)
# Collect the values to the driver program
acBalRDD.collect()

# Create account master tuples
acMasterTuples = acMasterRDD.map(lambda master: master.split(",")).map(lambda masterList: (masterList[0], masterList[1] + " " + masterList[2]))
# Collect the values to the driver program
acMasterTuples.collect()

# Create balance tuples
acBalTuples = acBalRDD.map(lambda trans: trans.split(",")).map(lambda transList: (transList[0], transList[1]))
# Collect the values to the driver program
acBalTuples.collect()

# Join the tuples
acJoinTuples = acMasterTuples.join(acBalTuples).sortByKey().map(lambda tran: (tran[0], tran[1][0],tran[1][1]))
# Collect the values to the driver program
acJoinTuples.collect()

# ------- Not included Section I in the slide -------
# Find the account name and balance
acNameAndBalance = acJoinTuples.map(lambda tran: (tran[1],tran[2]))
# Collect the values to the driver program
acNameAndBalance.collect()

from decimal import Decimal
# Find the account tuples sorted by amount
acTuplesByAmount = acBalTuples.map(lambda tran: (Decimal(tran[1]), tran[0])).sortByKey(False)
# Collect the values to the driver program
acTuplesByAmount.collect()

# Get the top element
acTuplesByAmount.first()

# Get the top 3 elements
acTuplesByAmount.take(3)

# Count by the key
acBalTuples.countByKey()

# Count all the records
acBalTuples.count()

# Print the contents of the account name and balance RDD
acNameAndBalance.foreach(print)

# Find the balance total using accumulator
balanceTotal = sc.accumulator(0.0)
balanceTotal.value

# Do the summation
acBalTuples.foreach(lambda bals: balanceTotal.add(float(bals[1])))

# Print the results
balanceTotal.value

# ------ Not included Section I in the slide End -------

# To use SQL command.
from pyspark.sql import SparkSession
from pyspark.sql import Row

# Creation of the list from where the RDD is going to be created
acTransList = ["SB10001,1000", "SB10002,1200", "SB10003,8000", "SB10004,400", "SB10005,300", "SB10006,10000", "SB10007,500", "SB10008,56", "SB10009,30","SB10010,7000", "CR10001,7000", "SB10002,-10"]
spark = SparkSession(sc)

acTransDF = sc.parallelize(acTransList).map(lambda trans: trans.split(",")).map(lambda p: Row(accNo=p[0], tranAmount=float(p[1]))).toDF()

acTransDF.createOrReplaceTempView("trans")

# Print the structure of the DataFrame
acTransDF.printSchema()
# Show the first few records of the DataFrame
acTransDF.show()

# Use SQL to create another DataFrame containing the good transaction records
goodTransRecords = spark.sql("SELECT accNo, tranAmount FROM trans WHERE accNo like 'SB%' AND tranAmount > 0")
# Register temporary table in the DataFrame for using it in SQL
goodTransRecords.createOrReplaceTempView("goodtrans")
# Show the first few records of the DataFrame
goodTransRecords.show()

# Use SQL to create another DataFrame containing the high value transaction records
highValueTransRecords = spark.sql("SELECT accNo, tranAmount FROM goodtrans WHERE tranAmount > 1000")
# Show the first few records of the DataFrame
highValueTransRecords.show()

# Use SQL to create another DataFrame containing the bad account records
badAccountRecords = spark.sql("SELECT accNo, tranAmount FROM trans WHERE accNo NOT like 'SB%'")
# Show the first few records of the DataFrame
badAccountRecords.show()

# Use SQL to create another DataFrame containing the bad amount records
badAmountRecords = spark.sql("SELECT accNo, tranAmount FROM trans WHERE tranAmount < 0")
# Show the first few records of the DataFrame
badAmountRecords.show()

# Do the union of two DataFrames and create another DataFrame
badTransRecords = badAccountRecords.union(badAmountRecords)
# Show the first few records of the DataFrame
badTransRecords.show()

# Calculate the sum
sumAmount = spark.sql("SELECT sum(tranAmount)as sum FROM goodtrans")
# Show the first few records of the DataFrame
sumAmount.show()

# Calculate the maximum
maxAmount = spark.sql("SELECT max(tranAmount) as max FROM goodtrans")
# Show the first few records of the DataFrame
maxAmount.show()

# Calculate the minimum
minAmount = spark.sql("SELECT min(tranAmount)as min FROM goodtrans")
# Show the first few records of the DataFrame
minAmount.show()

# Use SQL to create another DataFrame containing the good account numbers
goodAccNos = spark.sql("SELECT DISTINCT accNo FROM trans WHERE accNo like 'SB%' ORDER BY accNo")
# Show the first few records of the DataFrame
goodAccNos.show()

# Create the DataFrame using API for the high value transaction records
highValueTransRecords = goodTransRecords.filter("tranAmount > 1000")
# Show the first few records of the DataFrame
highValueTransRecords.show()

# Create the DataFrame using API for the bad account records
badAccountRecords = acTransDF.filter("accNo NOT like 'SB%'")
# Show the first few records of the DataFrame
badAccountRecords.show()

# Create the DataFrame using API for the bad amount records
badAmountRecords = acTransDF.filter("tranAmount < 0")
# Show the first few records of the DataFrame
badAmountRecords.show()

# Calculate the sum
sumAmount = goodTransRecords.agg({"tranAmount": "sum"})
# Show the first few records of the DataFrame
sumAmount.show()

# Calculate the maximum
maxAmount = goodTransRecords.agg({"tranAmount": "max"})
# Show the first few records of the DataFrame
maxAmount.show()

# Calculate the minimum
minAmount = goodTransRecords.agg({"tranAmount": "min"})
# Show the first few records of the DataFrame
minAmount.show()



