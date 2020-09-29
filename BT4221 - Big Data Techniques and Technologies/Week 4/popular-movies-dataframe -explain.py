
# We start by importing SparkSession, which is our new API in Spark for doing DataFrame adn DataSet operations.
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions

# We have our loadMovieName function. This is to create a map of movie IDs to movieNames, and that is unchanged from the earlier example. We are going to use the function to look up the movie names as we print out results at the end.
def loadMovieNames():
    movieNames = {}
    with open("ml-100k/u.ITEM") as f:
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1]
    return movieNames

# Create a SparkSession (Note that the config bit is only for Windows!) We give our app a name, called PopularMovies, and then have a SparkSession object that we can work with.
spark = SparkSession.builder.config("spark.sql.warehouse.dir", "file:///C:/temp").appName("PopularMovies").getOrCreate()

# Load up our movie ID -> name dictionary. We load up our dictionary of movie IDs to movieNames.
nameDict = loadMovieNames()

# We are going to start to get the sparkContext object that is part of SparkSession and calling textFile to import our unstructured data. u.data is just a text file as far as Spark is concerned. Now, if it were i a structured format, such as JSON, we would have done something like spark.read.json instead. This would have converted it directly into a DataFrame, which would be pretty cool. We hae to provide our won structure to it.
lines = spark.sparkContext.textFile("file:///SparkCourse/ml-100k/u.data")
# Convert it to a RDD of Row objects. We will call map by taking each line of the input and creating a row object consisting of a single column names movieID. Since all we are doing is counting how many times each movie ID occurs, the only column that we really care about is the movieID column. Thus, let's go ahead adn split the row, extract column number 2 and call it movieID.
movies = lines.map(lambda x: Row(movieID =int(x.split()[1])))

# We have an RDD called movies that consists of Row object, where each row consists of a single column named movieID. We can convert it into a DataFrame. This will allow Spark to treat it as a miniature database really, and this will give it all the opportunities of optimizaing queries. Remember that a DataFrame is a DataSet of Row objects as far as Spark terminology is concerned.
movieDataset = spark.createDataFrame(movies)

# Some SQL-style magic to sort all movies by popularity in one line. From the Row object we constructured, we now that movieID is the name of the column. Carrying on with the line, we count it up by movieID and order it by count in descending order. So, we can pass this extra parameter to orderBy that says I want you to go in descending order and get the most popular movies on the top. Then, you are caching the resulting DataSet to do more than one thing to it.
topMovieIDs = movieDataset.groupBy("movieID").count().orderBy("count", ascending=False).cache()

# Top 20 movies
topMovieIDs.show()

# Grab the top 10
top10 = topMovieIDs.take(10)

# Print the results. We are printing them up using nameDict, which is to actually map the names to human-readable movie names.
print("\n")
for result in top10:
    # Each row has movieID, count as above.
    print("%s: %d" % (nameDict[result[0]], result[1]))

# Stop the session
spark.stop()
