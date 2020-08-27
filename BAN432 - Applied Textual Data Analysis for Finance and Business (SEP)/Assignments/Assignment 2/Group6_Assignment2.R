####################################################################################
# BAN432 - Second assignment #

# Group 6:
# Kai Jing Zhou
# Lingling Tong
# Patrick Becher
# Susanne Tietze
# Yao Liu

rm(list = ls()) # delete environment
cat("\f") # delete console
setwd("/Users/patrick/Desktop/BAN432") # set working directory
load("company_index.RData") # load data
library(tidyr)
library(jsonlite)
library(dplyr)
library(tibble)
library(wordcloud)

####################################################################################
# Task 1: gather data from EDGAR #

months = c("2018/QTR4", "2019/QTR1", "2019/QTR2","2019/QTR3") # use quarters to access the last twelve months
totalfiles = 0
k10files = 0
for(i in months){
  # Build URL 
  web.url = paste0("https://www.sec.gov/Archives/edgar/full-index/", i , "/master.idx") # construct url
  
  # Download Index Files
  file.path = paste0(substr(i,1,4), "_", substr(i,6,9), ".txt") # file name
  download.file(web.url, file.path("/Users/patrick/Desktop/BAN432/IndexFiles", file.path), mode="wb") # download file
  
  # Read and Structure Index files 
  edgar.index.raw = readLines(web.url) # read file into R
  edgar.index = strsplit(edgar.index.raw[12:length(edgar.index.raw)], split="\\|") # split data according to "|"
  edgar.index = matrix(unlist(edgar.index), ncol = 5, byrow = T) # make a matrix
  edgar.index = as.data.frame(edgar.index, stringsAsFactors = F) # make a data frame
  colnames(edgar.index) = c("cik", "company.name", "form.type", "data.filed", "url") # column names
  
  # Read Company Files with Form 10-K
  edgar.index = subset(edgar.index, form.type=="10-K") # limit to "10-K"
  totalfiles = totalfiles + nrow(edgar.index)
  edgar.index = subset(edgar.index, edgar.index$cik %in% comp$cik) # limit to specific firms
  k10files = k10files + nrow(edgar.index)
  
  # Download 10-K Files 
  edgar.index$file.path = paste0("K10_", substr(i,1,4), "_", substr(i,6,9), "_", edgar.index$cik[1:nrow(edgar.index)], ".txt") # the name for the file 
  for(j in 1:nrow(edgar.index)){ # go over all files in the current index file
    file.path = edgar.index$file.path[j] # file name
    download.file(url = paste0("https://www.sec.gov/Archives/",edgar.index$url[j]), file.path("/Users/patrick/Desktop/BAN432/K10Files", file.path), mode="wb") # download file
  }
}


####################################################################################
# Task 2: clean the 10Ks #

# Download and Process Html Entities
html.url = "https://html.spec.whatwg.org/entities.json" # link
html.entities = fromJSON(html.url) # link is stored as JSON File 
html.entities = enframe(unlist(html.entities)) # make data easily accessible
html.entities = separate(html.entities, col = 1, sep = "\\.", into = c("name","type")) # separate columns
html.entities = filter(html.entities, grepl("characters", html.entities$type)==TRUE) # give out only specific columns
# Html enitites: it takes a lot of time to process and you do not really need it -> solution does not change much

# Read and Structur 10-K Files 
file_list = list.files("/Users/patrick/Desktop/BAN432/K10Files") # list all files in the folder
for(k in 1:length(file_list)){ #
edgar.10k.raw = readLines(paste0(file.path("/Users/patrick/Desktop/BAN432/K10Files",file_list[k])), encoding = "UTF-8") # load data

edgar.10k = edgar.10k.raw[grep(pattern = "^<TYPE>", edgar.10k.raw)[1]:grep(pattern = "^<TYPE>", edgar.10k.raw)[2]] # only use <TYPE>10-K
edgar.10k = edgar.10k[grep(pattern = "^<TEXT>", edgar.10k)[1]:grep(pattern = "^</TEXT>", edgar.10k)[1]] # subset over <TEXT>
edgar.10k = gsub("<.*?>", "",edgar.10k) # remove all html-tags

# Html enitites: 
for (h in 1:nrow(html.entities)){ # see html.entities
  edgar.10k = gsub(html.entities[[1]][h], html.entities[[3]][h], edgar.10k) #remove html-entities
}

edgar.10k = gsub("[[:digit:]]", "", edgar.10k) # remove numbers
edgar.10k = gsub("\\s+"," ",edgar.10k)  # remove excessive whitespace
edgar.10k = toString(edgar.10k) # make one big string
write.csv(edgar.10k, file.path("/Users/patrick/Desktop/BAN432/K10Structured", file_list[k])) # save the document
}

# Load Data
data=c()
cik=c()
file_list = list.files("/Users/patrick/Desktop/BAN432/K10Structured") # list all files in the folder
for(e in 1:length(file_list)){ 
  edgar = readLines(paste0(file.path("/Users/patrick/Desktop/BAN432/K10Structured",file_list[e])), encoding = "UTF-8") # load data
  data  = c(data, toString(edgar))
  company =  gsub(".+_(.+).txt", "\\1", file_list[e])
  cik = c(cik, company)
}
save("data", "cik", file = "assignment.Rdata") # Save data to easy access them later


####################################################################################
# Task 3: KWIC analysis #

# Process data
load("assignment.Rdata") # you can load our data
business.des = sapply(data, function(i) {scan(text = i, what = "character", quote = "")}) # We use sapply() to apply the scan() function to each of the texts. 

make.KWIC = function(index.env, business.des, n, doc.nr){ # Next, we define a function that constructs a tibble (data frame)  
  KWIC = tibble(left = sapply(index.env, function(i) {paste(business.des[(i-n):(i-1)], collapse = " ")}),
                keyword = business.des[index.env], 
                right = sapply(index.env, function(i) {paste(business.des[(i+1):(i+n)], collapse = " ")}),
                doc.nr = doc.nr,
                position.in.text = index.env/(length(business.des)*0.01))
  return(KWIC)
}

# Make KWIC Analysis and wordclouds
search = c("environment",  "governance", "social", "community", "safety", "responsibility", "health", "community", "planet", "employee", "shareholder", "emissions", "recycle",
           "customer", "sustainable", "sustainability", "diversity", "commitment", "impact", "security", "protection", "climate", "return", "privacy", "efficiency")

for (s in 1:length(search)){
  index.env = sapply(business.des, function(i) {grep(paste0("", search[s], ""), i, ignore.case =T)}) # Find the elements that matches the search term
  result = list() # Iterate over the lists 'index.env' and 'business.des' using the function 
  for(i in 1:length(business.des)){
    result[[i]] = make.KWIC(index.env[[i]], business.des[[i]], n = 3, doc.nr = i)
  }
merged.results = do.call("rbind", result) # Combine the tibbles into one, using do.call()
  
  
# Right
  # Find the most common words for right and left context
  merged.results$right %>%
    paste(collapse = " ") %>% # paste it into one long string
    scan(text = ., what = "character", quote = "") -> right.context # tokenize it with scan()
  # Clean text 
  right.context %>%
    tolower() %>% # convert to lower case
    gsub("^[[:punct:]]+|[[:punct:]]+$", "", .) %>% # remove punctuation in the beginning and in the end
    .[!. %in% tm::stopwords()] -> right.context.cleaned # remove stopwords (based on tm stopword list)
  # Convert text
  right.context.cleaned %>%
    table() %>% # Make a frequency list
    as_tibble() %>% # convert into a tibble
    arrange(desc(n)) -> input.cloud # descending order
  colnames(input.cloud) = c("word", "freq") # Give new column names
  filename = paste0(search[s],".png")
  png(file.path("/Users/patrick/Desktop/BAN432/Wordclouds",filename), 2000, 2000) # saves as PNG-File
  wordcloud(words = input.cloud$word[1:50], freq  = input.cloud$freq[1:50], scale = c(20,3)) # visualize as a wordcloud
  dev.off() # switches off the PNG-File

# Left 
  merged.results$left %>%
    paste(collapse = " ") %>% # paste it into one long string
    scan(text = ., what = "character", quote = "") -> left.context # tokenize it with scan()
  # Clean text 
  left.context %>%
    tolower() %>% # convert to lower case
    gsub("^[[:punct:]]+|[[:punct:]]+$", "", .) %>% # remove punctuation in the beginning and in the end
    .[!. %in% tm::stopwords()] -> left.context.cleaned # remove stopwords (based on tm stopword list)
  # Convert text
  left.context.cleaned %>%
    table() %>% # Make a frequency list
    as_tibble() %>% # convert into a tibble
    arrange(desc(n)) -> inputleft.cloud # descending order
  colnames(inputleft.cloud) = c("word", "freq") # Give new column names
  filename = paste0(search[s],"left", ".png")
  png(file.path("/Users/patrick/Desktop/BAN432/Wordclouds",filename), 2000, 2000) # saves as PNG-File
  wordcloud(words = inputleft.cloud$word[1:50], freq  = inputleft.cloud$freq[1:50], scale = c(30,5)) # visualize as a wordcloud
  dev.off() # switches off the PNG-File
}

# Terms 
# Good: governance, responsibility, community, employee, emissions, customer, safety, diversity, security, efficiency
# Bad: environment, social, safety, health, planet, shareholder, commitment, impact, protection, climate, return, privacy

####################################################################################
# Task 4: ESG score #

term = c("security", "employee", "customer", "sustainable", "efficiency", "footprint") # chosen terms for our score

score = data.frame(cik) # store the companies (order how files are loaded)
index.count=c() # needed for the loop
value = 1:length(cik) # ""
n = 0 # ""
for(l in 1:length(term)){
  index = sapply(business.des, function(i) {grep(paste0("", term[l], ""), i, ignore.case =T)}) # search for the term
  for(m in 1:length(cik)){
    index.count[m]=length(index[[m]])/length(business.des[[m]]) # relative word count
  }
  score = data.frame(score, index.count) # make a dataframe
  score = score[order(score[1+l+n], decreasing = T),] # order data frame
  score = data.frame(score, value) # make a dataframe
  n = n + 1
}

score.sub = score[,c(1,3,5,7,9,11,13)] # select columns
score.sub$sum = rowSums(score.sub[,2:length(score.sub)]) # sum relative word counts
score.merged = merge(x = score.sub, y = comp, by = "cik", all = F) # merge to compare to the given score
score.merged = score.merged[order(score.merged$sum),] # order data frame
table(score.merged$sustainable[1:100]) # compare Top100 companies from this ranking to the one by calvert

# Explanation:
# Calvert did a very SOPHISTICATED reviewed more than 200 Key-Factors and weighted industries etc. 
# With this approach I was able to match 45 companies in my Top100 that are also in Calvert´s Top100. 
# I think this is a good solution based on this very simple approach, i.e. looking only on one annual report, key-word based analysis, unweighted score etc.
# For the difference there could are several reasons: 
# - unability to relate suistanability to a key-word based analysis
# - companies talked about suistanability in previous annual reports more
# - companies are suistanable but do not mention it often in annual reports, e.g. more in newspapers, webpage, etc.
# - not suistanable companies talk a lot about suistanability


####################################################################################
# Optional: Provide a statistical test indicating whether your ESG score has the same information as the one by Calvert. #

# Fortunately, there is a significant relationship (p-value = 0.018)
fit = lm(score.merged$sustainable ~ score.merged$sum) 
summary(fit)

####################################################################################
