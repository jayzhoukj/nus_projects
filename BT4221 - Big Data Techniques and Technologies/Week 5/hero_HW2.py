
#You can use RDD or DataFrame
import findspark
findspark.init()
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions

conf = SparkConf().setMaster("local").setAppName("PopularHeroNetwork")
sc = SparkContext(conf = conf)

#countCoOccurenes will split up each line based on the space and return key/value pairs.
def countCoOccurences(line):
    elements = line.split()
    return (int(elements[0]), len(elements) - 1)

# parseNames will split based on the back-slash delimiter ('\'), extract hero ID and store it as an integer as a key. Then, it will encode thiings into UTF-8 format as a string. From this process, namesRDD will be a key/value RDD, where the key is hero ID , and the value is the name of hero.
def parseNames(line):
    fields = line.split('\"')
    return (int(fields[0]), fields[1].encode("utf8"))

# Load up your file into an RDD called names.
names = sc.textFile("hero-names.txt")
namesRdd = names.map(parseNames)

# We are loading up the social network data into a lines RDD.
lines = sc.textFile("/hero-network.txt")

# countCoOccurrences wil turn the input data into useful data.
pairings = lines.map(countCoOccurences)

# Heros can span multiple lines. Thus, reduceByKey add them all up together regarding the same ID.
# If we have two entries for one ID, we can add them together, and reduce them into a single entry. Thus, totalFriendsByCharacter itself a key/value RDD.

[ xxxx write your code xxxx ]

# We need to find the most appearanced hero.
[ xxxx write your code xxxx ]


# We can find the maximum key/value.
[ xxxx write your code xxxx ]

# We need to find the name to display.
[ xxxx write your code xxxx ]

print(mostPopularName + " is the most popular superhero, with " + \
    str(mostPopular[0]) + " co-appearances.")
