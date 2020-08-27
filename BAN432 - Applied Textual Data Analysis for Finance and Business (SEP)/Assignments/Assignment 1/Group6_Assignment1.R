######################################################################################################################################################
### Group 6: Assignment 1 ###

rm(list = ls()) # delete environment
cat("\f") # delete console

# Kai Jing Zhou
# Lingling Tong
# Patrick Becher
# Susanne Tietze

######################################################################################################################################################
### TASK 1 ###


# Load Data # 
web_page = readLines("https://en.wikipedia.org/wiki/Enron_scandal") # load the URL-Webpage into R

# Find the lines that contains "References" and "Further Reading". Only the first number is needed, because "Further Reading" follows directly 
find_line = grep("\\bid=\"References\"", web_page) # grep("\\bid=\"Further_reading\"", web_page)

# Commong feature: class="citation book". But we have to exclude citations that are not in the sections "References" and "Further Reading"
lines = grep("\\bclass=\"citation book\"", web_page) # extract all class="citation book" references
lines = lines[lines >= find_line] # build a subset based on lines that we want to use

store = web_page[lines] # Look at the data. We have eleven citations

# Common feauture: class=\"external text\"
external = gregexpr("class=\"external.+\".+?>", store) # give out only the part that belongs to the class=\"external text\"
match_external =regmatches(store, external) # ""
result1 = gsub(".+href=\"(.+)\".+","\\1" , unlist(match_external)) # only extract http string. Use unlist(m2) to consider more than one link in an element
result1

# There are two links in one line. One refers to an outdated file
store2 = unlist(match_external)
store2 = store2[grep("https", unlist(match_external))]
result2 = gsub(".+href=\"(.+)\".+","\\1" , unlist(store2)) # only extract http string. Use unlist(m2) to consider more than one link in an element
result2


######################################################################################################################################################
### TASK 2 ###

# Load Data # 
web_lines = grep(".+/wiki.+", web_page) # extract lines for performance gains

wiki= gregexpr("href=\"/wiki/.+\".+?</a>", web_page[web_lines]) # extract only those parts that refers to wikipedia pages
wiki_lines = regmatches(web_page[web_lines], wiki) # 
Name = gsub(".+title=\".+\">(.+)</a>","\\1" , unlist(wiki_lines))

# Process data
Name = gsub(pattern = "<bdi>(.+)</bdi>","\\1", Name) # just noise
Name = gsub(pattern = "<i>(.+)</i>","\\1", Name) # ""
Name = Name[-grep("<", Name)] # ""
Name = gsub(pattern = "&amp;", replacement = "&", Name) # ""
Name = Name[-grep("CS1 errors", Name)] # ""

# Delete the word "help"
Name = Name[Name!="help"] # title="Help:CS1 errors" is just incluced if links are not working?

result3 = data.frame(sort(table(Name), decreasing = T)[1:25])
result3

######################################################################################################################################################
### TASK 3: Password security ###


# Set working directory
# setwd("")

# Load file
passwords = readLines("passwords.txt")

# Function to test passwords
password_check = function(passwords){ 
  
  security_level = rep(0, length(passwords)) # vector with zeros to store numbers
  
  for (i in 1:length(passwords)){ # loop to test every element in the vector 
    
    if(nchar(passwords)[i] >= 8  &  grepl(" ", passwords[i]) == FALSE) # Test the two mandatory requirements. If fullfilled proceed to the next step
    { 
      if (grepl("[[:upper:]]", passwords[i] )) {security_level[i] = security_level[i]+1} # give for each requirement a point
      if (grepl("[[:lower:]]", passwords[i] )) {security_level[i] = security_level[i]+1} # ""
      if (grepl("[[:digit:]]", passwords[i] )) {security_level[i] = security_level[i]+1} # ""
      if (grepl("[[:punct:]]", passwords[i] )) {security_level[i] = security_level[i]+1} # ""
      if (security_level[i]==0) {security_level[i] = security_level[i]+1}
    }
    else {security_level[i]=1}
  }
  security_level = security_level-1 # due to the structure of the loop
  paste(passwords, security_level, sep = ": security level ") # put two vectors together
}

result4 = password_check(passwords) # call function
result4

######################################################################################################################################################