from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("PopularMovies")
sc = SparkContext(conf = conf)

lines = sc.textFile("xxxx/u.data")

# We call a mapper to split our data out and pulls out the movie ID from field number 1. We need to gain movies RDD that is nothing but a list of movie IDs. Each movie ID may occur frequently. Our main goal is to count the number of frequency.Mapper will extract the moview ID, put in a key/value pair where the key is the movie ID and the value is the number 1.
movies = lines.map(lambda x: (int(x.split()[1]), 1))

movieCounts = movies.reduceByKey(lambda x, y: x + y)
# We can use reduceByKey and add up all those 1 numbers together to get the count of how many times each movie appeared. We are going to group together and aggregate all of the values seen for movie ID and the number 1.

flipped = movieCounts.map( lambda (x, y) : (y, x) )
# We have key/value RDD, where the keys are the movie IDs. We want to sort it by the value, so we are going to use that same trick we did before wehre we flip things around to make the values the keys and the keys the values.

sortedMovies = flipped.sortByKey()
# We can use sortByKey to sort our RDD by the number of occurences.

# We can collect the result.
results = sortedMovies.collect()

for result in results:
    print(result)
