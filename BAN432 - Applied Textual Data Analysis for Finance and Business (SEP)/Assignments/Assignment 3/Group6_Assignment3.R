####################################################################################
# BAN432 Fall 2019 - Third assignment #

# Group 6:
# Kai Jing Zhou
# Lingling Tong
# Patrick Becher
# Susanne Tietze
# Yao Liu

rm(list = ls()) # delete environment
cat("\f") # delete console
setwd("/Users/patrick/Desktop/TextualData/15Assignment3") # set working directory
load("/Users/patrick/Desktop/TextualData/15Assignment3/data_assignment_3.Rdata") # load data
load("/Users/patrick/Desktop/TextualData/15Assignment3/shortcut.Rdata") # ""
library(dplyr) # load package
library(tm) # ""
library(slam) # ""


####################################################################################
# Task 1: Network analysis in a portfolio choice problem #
# Step 1 #

doc = data.frame(doc = 1:nrow(raw.data), cik = raw.data$cik, industry = raw.data$industry.fama.french.49, stringsAsFactors = F) # store data

doc.oil.firms = doc[doc$industry == "30 Oil", ] # id´s of oil firms 

all.wordclasses = paste0(section.1.pos[section.1.pos$doc_id %in% doc.oil.firms$doc, ]$token, collapse = " ") # all tokens
attr(all.wordclasses, "names") = "oil.firms" # give a name
nouns.adj = paste0(section.1.pos[section.1.pos$doc_id %in% doc.oil.firms$doc & section.1.pos$tag %in% c("NN", "NNS", "NNP", "NNPS", "JJ", "JJR", "JJS"), ]$token, collapse = " ") # only nouns and adjectives
attr(nouns.adj, "names") = "oil.firms" # give a name

mytext.oil.firms = list(all.wordclasses=all.wordclasses, nouns.adj=nouns.adj) # make a list


####################################################################################
# Step 2 #

doc.nonoil.firms = doc[doc$industry != "30 Oil", ] # id´s of nonoil firms

all.wordclasses = c() # store data
nouns.adj = c() # store data
for(i in 1:nrow(doc.nonoil.firms)){
  all.wordclasses[i] = paste0(section.1.pos[section.1.pos$doc_id == doc.nonoil.firms$doc[i], ]$token, collapse = " ") # all tokens
  nouns.adj[i] = paste0(section.1.pos[section.1.pos$doc_id == doc.nonoil.firms$doc[i] & section.1.pos$tag %in% c("NN", "NNS", "NNP", "NNPS", "JJ", "JJR", "JJS"), ]$token, collapse = " ") # only nouns and adjectives
}
attr(all.wordclasses, "names") = doc.nonoil.firms$cik # give a name
attr(nouns.adj, "names") = doc.nonoil.firms$cik # ""

mytext.non.oil.firms = list(all.wordclasses=all.wordclasses, nouns.adj=nouns.adj) # make a list


####################################################################################
# Step 3 #

allwordclasses = c(text.non.oil.firms$all.wordclasses, text.oil.firms$all.wordclasses) # concatenate the corresponding vectors
nounsandadjectives = c(text.non.oil.firms$nouns.adj, text.oil.firms$nouns.adj) # concatenate the corresponding vectors

# a) DTM based on all word classes with weighting and normalization
dtm.all.weight.normal = DocumentTermMatrix(Corpus(VectorSource(allwordclasses)), control = list(removePunctuation = T, stopwords = T, removeNumbers = T, tolower=T, stemming = F, wordLengths = c(3, 20), bounds = list(global = c(5,50)))) 
dtm.all.weight.normal = weightBin(dtm.all.weight.normal) # apply weights 
dtm.all.weight.normal$v = dtm.all.weight.normal$v / sqrt(row_sums(dtm.all.weight.normal^2)[dtm.all.weight.normal$i]) # apply normalization

# (b) DTM based on all word classes without any weighting/normalization
dtm.all = DocumentTermMatrix(Corpus(VectorSource(allwordclasses)), control = list(removePunctuation = T, stopwords = T, removeNumbers = T, tolower=T, stemming = F, wordLengths = c(3, 20), bounds = list(global = c(5,50)))) 

# (c) DTM based on only nouns and adjectives and with a weighting and normalization as in Hoberg/Phillips (2016)
dtm.na.weight.normal = DocumentTermMatrix(Corpus(VectorSource(nounsandadjectives)), control = list(removePunctuation = T, stopwords = T, removeNumbers = T, tolower=T, stemming = F, wordLengths = c(3, 20), bounds = list(global = c(5,50)))) 
dtm.na.weight.normal = weightBin(dtm.na.weight.normal) # apply weights 
dtm.na.weight.normal$v = dtm.na.weight.normal$v / sqrt(row_sums(dtm.na.weight.normal^2)[dtm.na.weight.normal$i]) # apply normalization

# (d) DTM based on only nouns and adjectives without any weighting/normalization
dtm.na = DocumentTermMatrix(Corpus(VectorSource(nounsandadjectives)), control = list(removePunctuation = T, stopwords = T, removeNumbers = T, tolower=T, stemming = F, wordLengths = c(3, 20), bounds = list(global = c(5,50)))) 


# Reasons for the choices in DTM: 
# terms appearance in documents: the more words one use, the higher similarity becomes, one inflate the similarity score but meaning does not become better
# lower case: does not matter how the word is written, only that it appears and thereby consider wrong written words
# punctuation: is not important for our analysis because we are interested in words, for us it is just noise
# stopwords: these words often appear in a document but does not have any specific meaning that would them make relevant for our analysis
# numerics: is not important for our analysis because we are interested in words, for us it is just noise
# word lengths: lower bound: words shorter than 3 letters do not have much meaning, upper bound: make sure that you do not a large string which is wrong written


####################################################################################
# Step 4 #

CosineSimilarity = function(A,B) { # function for CosineSimilarity
  sum(A * B) / sqrt(sum(A^2) * sum(B^2))
}

cik.reference = "oil.firms" # reference oil firms 
cik.nonoil = attributes(text.non.oil.firms$all.wordclasses)$names # all cik´s of non-oil firms

similarity = matrix(NA, ncol=5, nrow=length(cik.nonoil)) # store similarities 
for(i in 1:length(cik.nonoil)){ 
similarity[i,1] = cik.nonoil[i] # store cik name and similarities for all different dtm´s
similarity[i,2] = CosineSimilarity(dtm.all.weight.normal[dtm.all.weight.normal$dimnames$Docs == cik.reference, ], dtm.all.weight.normal[dtm.all.weight.normal$dimnames$Docs == cik.nonoil[i], ])
similarity[i,3] = CosineSimilarity(dtm.all[dtm.all$dimnames$Docs == cik.reference, ], dtm.all[dtm.all$dimnames$Docs == cik.nonoil[i], ])
similarity[i,4] = CosineSimilarity(dtm.na.weight.normal[dtm.na.weight.normal$dimnames$Docs == cik.reference, ], dtm.na.weight.normal[dtm.na.weight.normal$dimnames$Docs == cik.nonoil[i], ])
similarity[i,5] = CosineSimilarity(dtm.na[dtm.na$dimnames$Docs == cik.reference, ], dtm.na[dtm.na$dimnames$Docs == cik.nonoil[i], ])
}


####################################################################################
# Step 5 #

oil.portfolio.data = raw.data[raw.data$industry.fama.french.49 == "30 Oil", c(1,28:39)] # get data for all oil firms
oil.return =  col_means(oil.portfolio.data[ ,2:13]) # compute monthly averages 

correlations = c() # store data 
for(i in 2:ncol(similarity)){
  portfolio.firms = similarity[order(desc(similarity[,i])), ][1:25,1] # get ciks for different portfolios
  portfolio.data = raw.data[raw.data$cik %in% portfolio.firms, c(1,28:39)] # get data
  portfolio.return = col_means(portfolio.data[ ,2:13]) # compute monthly averages 
  correlations[i-1] = cor(oil.return, portfolio.return) # compute correlation coefficients
}
correlations = matrix(correlations, ncol=2) # store in a matrix 
rownames(correlations) = c("weightBin", "no.weight") # name rows
colnames(correlations) = c("all.wordclasses", "nouns.adj") # name colums
correlations # Correlations between the oil industry portfolio’s monthly returns and the four oil tracking portfolio’s return.


# All correlations are quite high and nearly similar. This shows that the approach works well to track oil industry´s development and that 
# the choices of weighting/no weighting of term frequencies and using all words vs. only using nouns and adjectives does not influence the result heavily. 
# The approaches that use only nouns and adjectives were more successfull because they deliver higher correlations in particular with weights/normalization applied.
# If all words are used the approach without using weights/normalization performed better. 

# Probable reasons: 
# If one use only nouns and adjectives the similarity between oil-related companies is becoming higher and therefore algorithm picks more likely these companies. 
# The weighting/normalization make sure that some large companies does not influence the similarity score too heavily. 
# If one uses all words than the weighting does not improve algorithm but works opposite. 


####################################################################################
# Bonus #

bonus.correlations = c() # store data s
for(i in 1:50){ # take 50 samples 
  bonus.sample = sample(cik.nonoil, 25, replace=F) # sample of 25 firms 
  bonus.portfolio.data = raw.data[raw.data$cik %in% bonus.sample, c(1,28:39)] # get data
  bonus.portfolio.return = col_means(bonus.portfolio.data[ ,2:13]) # compute monthly averages 
  bonus.correlations[i] = cor(oil.return, bonus.portfolio.return) # compute correlation coefficients
}
mean(bonus.correlations)

# Compared to the former approach the correlation is much lower. This shows that taking a random sample does not work well.
# A more more sophisticated approach is needed to track oil industry´s development. 


####################################################################################
