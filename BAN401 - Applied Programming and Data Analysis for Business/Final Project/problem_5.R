# Set working directory if the current working directory is not correctly set
if (getwd() != "C:/Users/Kai Jing/Desktop/NUS/Business (Accountancy)/NUS BAC/Sem 3.1/BAN401 - Applied Programming and Data Analysis For Business/Final Project"){
  setwd("C:/Users/Kai Jing/Desktop/NUS/Business (Accountancy)/NUS BAC/Sem 3.1/BAN401 - Applied Programming and Data Analysis For Business/Final Project")
}

# Clear workspace
rm(list = ls())

### Problem 5
# Read csv files containing the data for Table 3 and Table 4, using ';' as a separator
Table.3 <- read.csv('ban401_fuzzy-matching-table3.csv', sep = ';')
Table.4 <- read.csv('ban401_fuzzy-matching-table4.csv', sep = ';')

# Create column in Table 3 to store Total Granted Patents data
Table.5 <- Table.3
Table.5$Total.number.of.patents <- NA

# Check each company name in Table 3 against Table 4's company names in 'Applicant" column using agrep()
# Then, subset Table 4's Status column by the index result and obtain the total number of "Granted" patents, 
# and assign it to corresponding company in Table 3
for (i in 1:nrow(Table.5)){
  index <- agrep(Table.5$Company.name[i], 
                 Table.4$Applicant,
                 ignore.case = T)
  Table.5$Total.number.of.patents[i] <- sum(Table.4$Status[index] == "Granted")
}

Table.6 <- Table.4[Table.4$Status=='Granted',]
rownames(Table.6) <- NULL

for (i in 1:nrow(Table.6)){
  x <- agrep(Table.6$Applicant[i],Table.5$Company.name,ignore.case = T)
  
  if (length(x) != 0){
    Table.5$Total.number.of.patents[x] <- Table.5$Total.number.of.patents[x] + 1
  }
}

# Sort Table 3 according to the number of patents each company has in descending order
Table.5 <- Table.5[order(Table.5$Total.number.of.patents, decreasing = T),]
rownames(Table.5) <- NULL

head(Table.5, 5)
