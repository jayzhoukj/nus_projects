import sys
from pyspark import SparkConf, SparkContext
from math import sqrt

def loadMovieNames():
    movieNames = {}
    with open(r"C:\Users\Kai Jing\Desktop\NUS\Business (Accountancy)\NUS BAC\Sem 4.1\BT4221 - Big Data Techniques and Technologies\Class Materials\Week 6\u.item.txt",encoding="latin-1") as f:
        for line in f:
            fields = line.split('|')
            # print(fields[1])
            movieNames[int(fields[0])] = fields[1].encode().decode()
    return movieNames

def makePairs(user_ratings):
    (movie1, rating1) = user_ratings[1][0]
    (movie2, rating2) = user_ratings[1][1]
    return ((movie1, movie2), (rating1, rating2))

def filterDuplicates( userID_ratingsTuple ):
    # print(userID_ratingsTuple)
    (movie1, rating1) = userID_ratingsTuple[1][0]
    (movie2, rating2) = userID_ratingsTuple[1][1]
    return movie1 < movie2

def computeCosineSimilarity(ratingPairs):
    numPairs = 0
    sum_xx = sum_yy = sum_xy = 0
    for ratingX, ratingY in ratingPairs:
        sum_xx += ratingX * ratingX
        sum_yy += ratingY * ratingY
        sum_xy += ratingX * ratingY
        numPairs += 1

    numerator = sum_xy
    denominator = sqrt(sum_xx) * sqrt(sum_yy)

    score = 0
    if (denominator):
        score = (numerator / (float(denominator)))

    return (score, numPairs)


conf = SparkConf().setMaster("local[*]").setAppName("MovieSimilarities")
sc = SparkContext(conf = conf)
# sc.setLogLevel("WARN")
# We will load up the dictionary of movie names. If you look at the loadMovieNames script up, you can see that
# it is just returning a python dictionary that maps movie IDs to human-readable movie names so we can look at them more easily. If you see line 11, we can actually display them in our Terminal-that's all that decode stuff is doing. The dictionary will be used at the very end for the final display

print("\nLoading movie names...")
nameDict = loadMovieNames()
# print(nameDict[int(sys.argv[1])])

# Load up our source data of moview rations. It includes user ID, moview ID, rating and timestamp. This wil go into a data RDD.
data = sc.textFile(r"C:\Users\Kai Jing\Desktop\NUS\Business (Accountancy)\NUS BAC\Sem 4.1\BT4221 - Big Data Techniques and Technologies\Class Materials\Week 6\u.data.txt")

# Map ratings to key / value pairs: user ID => movie ID, rating
# We start off by splitting the data on whitespace into inividual fields, and then we map it again into the format we want. This process will going to give us back an RDD that has user ID as the key and the values will be these composite values of movie ID and ratings. Thus, we can have key/value RDD now. The key is user ID and the values are movie-rating pairs.
ratings = data.map(lambda l: l.split()).map(lambda l: (int(l[0]), (int(l[1]), float(l[2]))))

print("\n\n ratings rdd: ")
print(ratings.take(5))
print('\n')
# Emit every movie rated together by the same user.
# Self-join to find every combination. We are using self-join operation to find every combination of movies that were rated together by the same user.
# Still, the key is user ID and values are every possible combination of movie rating pairs that user watched.
joinedRatings = ratings.join(ratings)

# At this point our RDD consists of userID => ((movieID, rating), (movieID, rating))
# Filter out duplicate pairs
# We need to eliminate duplicates because of those possible permutations. We can have the same movie twice in a different order, and get the same movie related to the same movie.
#filterDuplicates function simply enforces that we only return pairs where movie 1 is less then movie 2. We enforce only one ordering of the movie pairs that are in sorted order, and we also eliminate pairs where movie 1 is the sma thing as movie 2.

uniqueJoinedRatings = joinedRatings.filter(filterDuplicates)

# Now key by (movie1, movie2) pairs.
moviePairs = uniqueJoinedRatings.map(makePairs)

# We now have (movie1, movie2) => (rating1, rating2)
# Now collect all ratings for each movie pair and compute similarity
# We need to shuffle things around. We are looking at the similarities between unique pairs of movies. We are running another map operatoin on that to make the new key movie pair itself. Thus, makePair map function does. It extracts the movie and rating for each pair of the input RDD and outputs a new key/value RDD where the key is the movie pair and the value is the ratings for that movie pair.
moviePairRatings = moviePairs.groupByKey()

# We now have (movie1, movie2) = > (rating1, rating2), (rating1, rating2) ...
# Now collect all ratings for each movie pair and compute similarity
# This is to determine the similarity score betwen these two movies.
# It is sort of a cosine-like function, a strong similarity will be a rather high number of close to 1.We are going to cache that result because we are using the movie pair of similarities RDD more than once. Without cache(), we need to go back and recompute the whole process one by one.
moviePairSimilarities = moviePairRatings.mapValues(computeCosineSimilarity).cache()
print("\n\n",moviePairSimilarities.take(10),"\n\n")
# Save the results if desired
# moviePairSimilarities.sortByKey()
# moviePairSimilarities.saveAsTextFile("movie-sims")

# Extract similarities for the movie we care about that are "good".
if (len(sys.argv) > 1):

#defning the similarity score and the minimum number of people watching the same movie.
    scoreThreshold = 0.97
    coOccurenceThreshold = 50

 # If we provide an argument to the script, we are looking for the movie ID.
    movieID = int(sys.argv[1])
    # print("MovieID: ",movieID)
    # Filter for movies with this sim that are "good" as defined by
    # our quality thresholds above
    # For example, if we pass in movie ID 50 (Star wars), we run another filter on my simliarities result to extract only the similarities that include Star Wars in the pair.
    filteredResults = moviePairSimilarities.filter(lambda pair_sim: \
        (pair_sim[0][0] == movieID or pair_sim[0][1] == movieID) \
        and pair_sim[1][0] > scoreThreshold and pair_sim[1][1] > coOccurenceThreshold)
    print()
    print("\n\n",filteredResults.take(5),"\n\n")
    # print("\n")
    # Sort by quality score. We sort the final result by the quality score. We are using the descending order adn take the top 10.
    results = filteredResults.map(lambda pair_sim: (pair_sim[1], pair_sim[0])).sortByKey(ascending = False).take(10)

    print("Top 10 similar movies for " + nameDict[movieID])
    for result in results:
        (sim, pair) = result
        # Display the similarity result that isn't the movie we're looking at
        similarMovieID = pair[0]
        if (similarMovieID == movieID):
            similarMovieID = pair[1]
        print(nameDict[similarMovieID] + "\tscore: " + str(sim[0]) + "\tstrength: " + str(sim[1]))

# command: spark-submit /xxYour file pathxx/similarities.py 50 on terminal -> movie ID =50 is the one that I would like to concern.
