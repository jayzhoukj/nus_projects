#! /usr/bin/env python3


# You can use python's built-in json module for converting python objects into json data and back. It is for json string in case that we use.
import re, json
# log is used for rating, as it is too big.
from math import log2, log10, ceil
from functools import partial
from pyspark import SparkContext

# We will round the number off to the nearest five-poin interval out of personal preference. You can omit this step or round off to a larger number such as 10 or 50 if you like.
def ceil5(x):
    return ceil(x/5)*5

# winner and looser implies more connection.
def get_winner_loser(match):
  ms = match.split(',')
  # Put the loser in first position, winner in second
  return (ms[20], ms[10])

#returns the number of items: a function to initializing to the original value 100. dict having key and value needs to have initial value.
def initialize_voting(losses):
    return {'losses': losses,
            'n_losses': len(losses),
            'rating': 100}

# the key for rating will be 0 to initialize dict.
def empty_ratings(d):
  d['rating'] = 0
  return d

# The following process is to do "traverse", meaning  that acc, nxt, and i will be fed by input data. i will be from 0 to 7, just iterate 7 time.

def allocate_points(acc, nxt, i):
    # We split the webpage into a key adn vaue becuase we had the webpage data stored as a two-tuple coming out of our .mapValues step.
  k,v = nxt
  # Next, we calculate the boost that each webpage which gains more rating will receive. Each webpage allocates its entire rating uniformly to all those which gains more rating. This means that the amount of the boost a webpage receives by gaining more is equal to the webpage rating divided by their number of losses. To prevent a divide by zero error, we add a small value to the number of losses a webpage has, in the event that it does not loss.
  if i == 0:
    boost = 100 / (v['n_losses']+.01)
    # if i is not equal to 0.
  else:
    boost = v['rating'] / (v['n_losses'] + .01)

  # Then, we allocate those points to each webpage which gains more rating to update. we do this by setting the opposing webpage rating equal to their current rating + boost factor. We return the accumulator and move on to the next webpage.
  # feed the value of key in losses into loss. If loss is not included in key of acc, we can make new value. acc[loss] will be initialized. if you have, get the key of loss from acc' dict. loss will be from the list, or {}, and get 0 rating value. Then, return acc(  = opp_rating + boost )
  for loss in v['losses']:
    if loss not in acc.keys():
      acc[loss] = {'losses':[], 'n_losses': 0}
       opp_rating = acc.get(loss,{}).get('rating',0)
    acc[loss]['rating'] = opp_rating + boost
  return acc

# feed k and v to b.
# We need to join dicts with the keys as values, such that the resulting dic has all the keys of both dicts and the values are the sum of the values.
# We will update dict that we aren't looping through. If we do not find a key from the dict we are looping through in the other, we will update the other so that key is equal to the value from our looping dict. Then, we will return the dict we did not loop through.
def combine_scores(a, b):
  for k,v in b.items():
  # if there is no k, get k from a and b
    try:
      a[k]['rating'] = a[k]['rating'] + b[k]['rating']
  # if there is not key, just feed.
    except KeyError:
      a[k] = v
  return a


#The if __name__ == "__main__" tells Python only to use this code if it’s called directly
as a script.
if __name__ == "__main__":
  sc = SparkContext(appName="WikiMap")
  entries = sc.textFile("wikipedia_edges.txt")
  xs = entries.flatMap(lambda x:x.split('\n'))\
                 .map(lambda x:x.split('\t'))\
                 .groupByKey()\
                 .mapValues(initialize_voting)


# iterate 7 times. People just do 7 times.
  for i in range(7):
    if i > 0:
      
      # To get an RDD, we need to explicitly convert the items of that dict into an RDD using .parallelize method from SparkContext: sc. Once our iteration is comoplete, we will ahve a dict with webpages as keys.
      xs = sc.parallelize(zs.items())
      
    #Before reducing, we need to set up our accumulating variable: acc. This is the variable that holds all webpages and their ratings. To get this variable, we will empty the ratings of all the keys from our dict of dicts(dictionaries). This will give each webpage a fresh new rating of 0 at the beginning of each PageRank.
    acc = dict(xs.mapValues(empty_ratings).collect())
    # send allocate point to i.
    #agg_f gets the return value of acc
    agg_f = partial(allocate_points, i=i)
    
    #acc: We will store the points for each web page in a dict that has some of the meta data about rating.
    #agg_f: We will allocate rating by having all the webpage points.
    #combine_scores: Once we allocate rating for each webpage, we then sum up the points(i.e., acc and agg_f) to arrive at the total rating. This is our combination function for aggregation.
    zs = xs.aggregate(acc, agg_f, combine_scores)

# rating include list, or [ ]. iterate item() times stored in zs.
  ratings = [(k,v['rating']) for k,v in zs.items()]
  
 # the number of letters is less than 30. The number of player is 50.
 # In general, people use log function for rating, as it is too big.
  for player, rating in sorted(ratings, key=lambda x: x[1], reverse=True)[:50]:
    print('{:<30}{}\t{}'.format(player,
                                round(log2(rating+1), 1),
                                ceil5(rating)))
