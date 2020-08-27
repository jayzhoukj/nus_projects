### TASK 1
## Set working directory
if (getwd() != "C:/Users/Kai Jing/Desktop/NUS/Business (Accountancy)/NUS BAC/Sem 3.1/BAN432 - Applied Textual Data Analysis for Business and Finance/Assignment 2"){
  setwd(paste0(getwd(),"/Assignment 2"))
}

## Load required packages
require(edgar)
require(tm)
require(wordcloud)
require(dplyr)

load("company_index.Rdata")

y <- 2018
q <- 4
web.url <- paste0("https://www.sec.gov/Archives/edgar/full-index/",
                  y, "/QTR", q, "/master.idx")

edgar.index.raw <- readLines(web.url)
edgar.index.raw[1:20]

edgar.index <- strsplit(edgar.index.raw[12:length(edgar.index.raw)], 
                        split = "|", 
                        fixed = T)

edgar.index <- matrix(unlist(edgar.index), ncol = 5, byrow = T)

edgar.index <- data.frame(edgar.index, stringsAsFactors = F)

colnames(edgar.index) <- c("cik", "company.name", "form.type", "date.filed", "url")

y <- 2019

for (q in 1:3){
  web.url <- paste0("https://www.sec.gov/Archives/edgar/full-index/",
                    y, "/QTR", q, "/master.idx")
  
  edgar.index.raw.2 <- readLines(web.url)
  edgar.index.raw.2[1:20]
  
  edgar.index.2 <- strsplit(edgar.index.raw.2[12:length(edgar.index.raw.2)], 
                          split = "|", 
                          fixed = T)
  
  edgar.index.2 <- matrix(unlist(edgar.index.2), ncol = 5, byrow = T)
  
  edgar.index.2 <- data.frame(edgar.index.2, stringsAsFactors = F)
  
  colnames(edgar.index.2) <- c("cik", "company.name", "form.type", "date.filed", "url")
  
  edgar.index <- rbind(edgar.index, edgar.index.2)
}

edgar.index <- edgar.index[edgar.index$form.type == "10-K", ]
edgar.index <- subset(edgar.index, form.type == "10-K")

edgar.index <- edgar.index[edgar.index$cik %in% comp$cik,]

edgar.index$file.path <- paste0("Data/K10_", 1:nrow(edgar.index), ".txt")
edgar.index$file.name <- substr(edgar.index$file.path, 6, 20)

# write.csv(edgar.index, "edgar_index.csv")

# for(i in 1:nrow(edgar.index)){
#   # download.file
#   download.file(url = paste0("https://www.sec.gov/Archives/",
#  lolocate_cate                            edgar.index$url[i]),
#                 destfile = edgar.index$file.path[i],
#                 mode = "wb")
# }

### TASK 2
k10.files <- list.files("Data")

for (i in k10.files){
  temp <- readLines(paste0("Data/", i))

  end.index <- match(grep("<TYPE>10-K", temp), grep("<TYPE>", temp))+1

  temp.2 <- temp[grep("<TYPE>10-K", temp):grep("<TYPE>", temp)[end.index]]

  temp.2 <- temp.2[grep("<TEXT>", temp.2):grep("</TEXT>", temp.2)]
  
  temp.2 <- gsub("<.+?>", " ", temp.2)
  temp.2 <- gsub("&.+?;", "", temp.2)
  temp.2 <- gsub("[[:digit:]]", "", temp.2)
  temp.2 <- paste(temp.2, collapse = " ")
  temp.2 <- gsub("\\s+", " ", temp.2)

  writeLines(temp.2, paste0("Data_cleaned/", i))
}

## Cleaning downloaded text files
temp <- readLines("Data/K10_1.txt")

end.index <- match(grep("<TYPE>10-K", temp), grep("<TYPE>", temp))+1

temp.2 <- temp[grep("<TYPE>10-K", temp):grep("<TYPE>", temp)[end.index]]

temp.2 <- temp.2[grep("<TEXT>", temp.2):grep("</TEXT>", temp.2)]

temp.2 <- gsub("<.+?>", " ", temp.2)
temp.2 <- gsub("&.+?;", "", temp.2)
temp.2 <- gsub("[[:digit:]]", "", temp.2)
temp.2 <- paste(temp.2, collapse = " ")
temp.2 <- gsub("\\s+", " ", temp.2)

writeLines(temp.2, "K10_1.txt")

### Preliminary Textual Analysis
keywords <- readLines("keywords_cleaned.txt")
edgar.index <- read.csv("edgar_index.csv")

## Loading all the K10 .txt files into a corpus for analysis
folder <- "Data_cleaned"
filelist <- list.files(path = folder, pattern = ".txt$")
filelist <- paste(folder, "/", filelist, sep="")
a <- lapply(filelist, FUN = readLines)
corpus <- sapply(a , FUN = paste, collapse = " ")

x <- scan(text = corpus[1],
          what = "character",
          quote = "")
head(x)

business.des <- sapply(corpus, function(i) scan(text = i,
                                                what="character",
                                                quote = ""))

head(business.des[[1]])

index.env <- sapply(business.des,
                    function(i) grep("diversity", i))

index.env[[1]]

i <- 1875
n <- 4
paste(business.des[[1]][(i-n):(i-1)], collapse = " ")

make.KWIC <- function(index.env, business.des, n, doc.nr){
  KWIC <- tibble(left = sapply(index.env,
                               function(i) {paste(business.des[(i-n):(i-1)], collapse = " ")}),
                 keyword = business.des[index.env], 
                 right = sapply(index.env,
                                function(i) {paste(business.des[(i+1):(i+n)], collapse = " ")}),
                 doc.nr = doc.nr,
                 position.in.text = index.env/(length(business.des)*0.01))
  return(KWIC)
}

result <- list()

for(i in 1:length(business.des)){
  result[[i]] <- make.KWIC(index.env[[i]],
                           business.des[[i]],
                           n = 3,
                           doc.nr = i)
}

result[[1]]
result[[5]]

merged.results <- do.call("rbind", result)

merged.results$right %>%
  paste(collapse = " ") %>%
  scan(text = .,
       what = "character",
       quote = "") -> right.context

right.context[1:50]

right.context %>%
  tolower() %>%
  gsub("^[[:punct:]]+|[[:punct:]]+$", "", .) %>%
  .[!. %in% tm::stopwords()] -> right.context.cleaned

right.context.cleaned[1:50]

right.context.cleaned %>%
  table() %>%
  as_tibble() %>%
  arrange(desc(n)) -> input.cloud

colnames(input.cloud) <- c("word", "freq")

filename <- "wordcloud1.png"
png(filename, 2000, 2000)
wordcloud(words = input.cloud$word[1:80],
          freq  = input.cloud$freq[1:80],
          scale = c(30,3))
dev.off()

custom.stopwords <- c("laws","regulations","health","safety",
                      "remediation", "matters",
                      "compliance","liabilities", "including")

input.cloud %>%
  filter(!word %in% custom.stopwords) -> input.cloud.2

filename <- "wordcloud2.png"
png(filename, 2000, 2000)
wordcloud(words = input.cloud.2$word[1:80],
          freq = input.cloud.2$freq[1:80],
          scale = c(20,2))
dev.off()

------------------------------------------------------------------------------------

### Further Analysis
grep("environmental protection", corpus)

m <- gregexpr(".{100}environmental protection.{20}", corpus[[58]])
regmatches(corpus[[58]], m)

# Step 1: rearrange the tibble according to the column
#         "position.in.text"
merged.results %>% 
  arrange(position.in.text) -> merged.results.sorted

# Step 2: Divide the rows to fall into 1 out of ten categories
intervals <- cut(merged.results.sorted$position.in.text, breaks = 10) #try 100 breaks
levels(intervals)

# Step 3: Make a barplot basd on "intervals"
plot(intervals,
     xlab = "Intervals: 0 = first word, 100 = last word",
     ylab = "Number of occurences",
     main = "Occurences of 'environment.*' within the documents")

# Testing significance of relationship between "environment" and "law" or "regulation"
fit <- lm(merged.results$position.in.text ~ grepl("(law)|(regulation)", merged.results$right))
summary(fit)

# -----------------------------------------------------------------------------
#### EXPERIMENTATION
aaa <- readLines("Data/K10_1.txt")
bbb <- aaa[grep("^<TYPE>",aaa)]

fit.2 <- lm(score.merged$sustainable ~ score.merged$sum)
summary(fit.2)