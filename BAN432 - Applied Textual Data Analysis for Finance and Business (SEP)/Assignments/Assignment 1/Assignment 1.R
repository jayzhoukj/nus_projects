# Set Working Directory
if (getwd() != "C:/Users/Kai Jing/Desktop/NUS/Business (Accountancy)/NUS BAC/Sem 3.1/BAN432 - Applied Textual Data Analysis for Business and Finance/Assignment 1") {
  setwd(paste0(getwd(),"/Assignment 1"))
}

# Task 1
html.wiki <- readLines("https://en.wikipedia.org/wiki/Enron_scandal")

idx <- grep("\\bid=",html.wiki) # narrow down all lines containing id tags
id.references <- grep("\\bid=\"References",html.wiki) # 
id.further.reading <- grep("\\bid=\"Further_reading",html.wiki)
# print(id.references %in% idx)

references.position <- which(idx == id.references)
further.reading.position <- which(idx == id.further.reading)

html.cleaned1 <- html.wiki[idx[references.position]:(idx[further.reading.position+1]-1)]

for (i in 1:length(html.cleaned1)){
  line.text <- html.cleaned1[i]
  m <- gregexpr("\\bhref=\"https:.+?\"",line.text)
  link.extracted <- regmatches(line.text,m)
  if (identical(link.extracted[[1]],character(0))){
    next()
  } else {
    print(substr(link.extracted[[1]],7,nchar(link.extracted[[1]])-1))
  }
}

# Task 2
html.wiki <- readLines("https://en.wikipedia.org/wiki/Enron_scandal")

wikix <- grep("href=\"/wiki/",html.wiki)
relevant.wiki <- html.wiki[wikix]
m <- gregexpr("href=\"/wiki/.+\".+?</a>",relevant.wiki)
relevant.wiki <- regmatches(relevant.wiki,m)

titles.extracted <- gsub(".+title=\".+\">(.+)</a>","\\1",unlist(relevant.wiki))
titles.extracted <- gsub("<bdi>(.+)</bdi>","\\1",titles.extracted)
titles.extracted <- gsub("<i>(.+)</i>","\\1",titles.extracted)

# titles.extracted <- lapply(regmatches(relevant.wiki,m),
#                            FUN = function(x){gsub(".+>(.+)<","\\1",x)})

titles.cleaned <- list()

for (i in 1:length(titles.extracted)){
  titles.cleaned <- c(titles.cleaned,titles.extracted[[i]])
}

titles.cleaned2 <- unlist(titles.cleaned, recursive = T)
titles.cleaned3 <- titles.cleaned2[-(grep("<",titles.cleaned2))]
titles.cleaned4 <- titles.cleaned3[!(titles.cleaned3==" ")]
titles.cleaned5 <- titles.cleaned4[-(grep("Wikipedia",titles.cleaned4,ignore.case = T))]
titles.cleaned6 <- titles.cleaned5[!(titles.cleaned5=="help")]
titles.cleaned6 <- gsub("&amp;","&",titles.cleaned6)
# titles.cleaned7 <- titles.cleaned6[-(grep("[[:digit:]]",titles.cleaned6))]

results <- sort(table(titles.cleaned6),decreasing=T)
print(head(as.data.frame(results),25))

# Task 3
pw.list <- readLines("passwords.txt")

for (i in 1:length(pw.list)){
  if ((nchar(pw.list[i])>=8) & !(grepl(" ",pw.list[i]))){
    if (grepl("[[:upper:]]",pw.list[i]) + 
        grepl("[[:lower:]]",pw.list[i]) + 
        grepl("[[:digit:]]",pw.list[i]) + 
        grepl("[[:punct:]]",pw.list[i]) == 0){
      print(paste0(pw.list[i],": security level 0"))
    } else {
      security.level <- 
        grepl("[[:upper:]]",pw.list[i]) + 
        grepl("[[:lower:]]",pw.list[i]) + 
        grepl("[[:digit:]]",pw.list[i]) + 
        grepl("[[:punct:]]",pw.list[i]) - 1
      print(paste0(pw.list[i],": security level ",as.character(security.level)))
    }
  } else {
    print(paste0(pw.list[i],": security level 0"))
  }
}
