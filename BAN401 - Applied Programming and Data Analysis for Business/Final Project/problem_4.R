# Set working directory if the current working directory is not correctly set
if (getwd() != "C:/Users/Kai Jing/Desktop/NUS/Business (Accountancy)/NUS BAC/Sem 3.1/BAN401 - Applied Programming and Data Analysis For Business/Final Project"){
  setwd("C:/Users/Kai Jing/Desktop/NUS/Business (Accountancy)/NUS BAC/Sem 3.1/BAN401 - Applied Programming and Data Analysis For Business/Final Project")
}

# Clear workspace
rm(list = ls())

### Problem 4
# Create a list of all the available denominations
Card.Points <- c(1, 2, 5, 10, 20, 50, 100)

# Set the base case for the number of combinations where no denominations of points are used
Base.Case <- c(c(1), rep(0, 200))

# Create a matrix detailing the number of combinations for all the points leading up to 200
# Then, fill in the matrix with number of combinations for that total points (in the column) 
# by deciding if the corresponding denomination in the Points List is used or not
Matrix.Sol <- matrix(nrow = 7, ncol = 201, byrow = T)
Matrix.Sol <- rbind(Base.Case, Matrix.Sol)
rownames(Matrix.Sol) <- c('{}',
                          '{1}',
                          '{1,2}',
                          '{1,2,5}',
                          '{1,2,5,10}',
                          '{1,2,5,10,20}',
                          '{1,2,5,10,20,50}',
                          '{1,2,5,10,20,50,100}')
colnames(Matrix.Sol) <- 0:200

for (i in 2:nrow(Matrix.Sol)){
  for (j in 1:ncol(Matrix.Sol)){
    if (j-1 < Card.Points[i-1]){
      Matrix.Sol[i,j] <- Matrix.Sol[i-1,j]
    } else{
      Matrix.Sol[i,j] <- Matrix.Sol[i-1,j] + Matrix.Sol[i,(j-Card.Points[i-1])]
    }
  }
}

cat('There are', as.character(Matrix.Sol[nrow(Matrix.Sol), ncol(Matrix.Sol)]), 'possible scenarios to buy one "2 megapoints"-card.')
