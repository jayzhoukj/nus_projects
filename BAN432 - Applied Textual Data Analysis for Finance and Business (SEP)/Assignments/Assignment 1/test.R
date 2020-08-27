a <- "Hello, World! This is an example of a <i>test</i> sentence"
gsub("\\b<i>(.+)<","\\1",a)
