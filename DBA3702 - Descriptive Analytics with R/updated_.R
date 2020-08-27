## PART 1: DATA WRANGLING AND CLEANING, REGRESSION AND ANOVA ANALYSIS

#import relevant library 
library(readr)
library(dplyr)
library(ggplot2)
library(ggmap)
library(ggthemes)
library(tidyr)
library(gplots)
library(leaflet)
library(chron)
library(reshape2)

setwd(getwd())

#import kaggle data 
StationData <- read_csv("station.csv")
TripData <- read_csv("trip.csv")
WeatherData <- read_csv("weather.csv")

if (!("Status9" %in% ls())) {
  if (file.exists("Data_cleaned.csv")) {
    Status9 <- read_csv("Data_cleaned.csv")
  } else {
    StatusData <- read_csv("status.csv")#import bike station status data
    
    StatusData$Year <- as.numeric(substr(StatusData$time,1,4)) #extract year and  form a new column
    StatusData <- StatusData[StatusData$Year==2014,] #only analysing in year 2014
    StatusData$Date <- paste0(substr(StatusData$time,9,10),"/",substr(StatusData$time,6,7),"/",substr(StatusData$time,1,4)) #add date
    StatusData$Hour <- as.numeric(substr(StatusData$time,12,13)) #add hour column
    StatusData$Min <- as.numeric(substr(StatusData$time,15,16)) #add minute column
    
    StatusData <- StatusData[,-4] #remove original time column
    StatusData$Date <- as.Date(StatusData$Date, "%d/%m/%Y")
    Status2 <- full_join(StatusData,StationData[,c(-7)],by=c("station_id"="id"))
    
    Status3 <- Status2[,-2]
    Status4 <- Status2[,-3]
    
    Status5 <- Status3 %>%
      group_by(station_id, Date, Year, Hour, name, lat, long, dock_count, city) %>%
      summarize(Average_Docks = mean(docks_available)) 
    
    Status6 <- Status4 %>%
      group_by(station_id, Date, Year, Hour, name, lat, long, dock_count, city) %>%
      summarize(Average_Bikes = mean(bikes_available))
    
    Status7 <- full_join(Status6, Status5)
    
    Status7$Usage_Rate <- Status7$Average_Docks/(Status7$Average_Bikes + Status7$Average_Docks)
    
    Status7$Date <- as.Date(Status7$Date, "%d/%m/%Y")
    
    WeatherData$date <- as.Date(WeatherData$date, "%m/%d/%Y")
    WeatherData$Year <- as.numeric(strftime(WeatherData$date, "%Y"))
    
    WeatherData <- WeatherData[WeatherData$Year==2014,]
    Status8 <- full_join(Status7,WeatherData,by=c("Date"="date"))
    
    na_count <- sapply(Status8, function(y) sum(length(which(is.na(y)))))
    na_count <- data.frame(na_count)
    
    Status9 <- Status8[complete.cases(Status8[,c("mean_temperature_f","mean_humidity","cloud_cover")]),]
    
    names(Status9)[names(Status9) == 'Year.x'] <- 'Year'
    Status9 <- Status9[,-ncol(Status9)]
    
    write.csv(Status9, file = "Data_cleaned.csv", row.names = FALSE)
  } 
}

#Identifying Interaction between Variables
cor(Status9[,c("mean_temperature_f","mean_humidity","cloud_cover")], use="complete")

## CONCLUSION: No interaction between the three independent variables (Interaction if correlation coefficient > 0.8)

# Multiple ANOVA
anova.twoway <- aov(Usage_Rate ~ mean_temperature_f + mean_humidity + cloud_cover, data = Status9)
summary(anova.twoway)

# Multiple Linear Regression
MLRModel <- lm(Usage_Rate ~ mean_temperature_f + mean_humidity + cloud_cover, data=Status9)
summary(MLRModel)

## PART 2: geo-spatial VISUALIZATION

#check the location of each bike station first
register_google(key='AIzaSyBKNZLfGl7FCDNmIhZmibexeWPBKl5XWXI')
bay_area_map<-get_map(location = c(mean(StationData$long),mean(StationData$lat)),source='google',zoom=10)
# dev.off()
ggmap(bay_area_map)+
  geom_point(data=StationData,aes(x=long,y=lat,color=city,size=dock_count),alpha=0.5)+
  ggtitle('Bike Stations in Bay Area')+
  theme_map()

leaflet()%>%addTiles() %>%
  addMarkers(data =StationData, lng = ~long, lat = ~lat,popup = ~name,
             clusterOptions = markerClusterOptions())
#We can see the stations are mainly located at 5 different cities in this area

#now, let's look at trips data
#firstly, filter trips with arrive/departure stations that are not in the 'stationd data set'
stations<-union(unique(TripData$end_station_name),unique(TripData$start_station_name))

setdiff(unique(TripData$start_station_name),StationData$name)
sta<-setdiff(unique(TripData$end_station_name),StationData$name) #identified 4 stations, remove them

tripdata<-TripData[(!TripData$start_station_name %in% sta & !TripData$end_station_name%in% sta),]

#clean the trip data, such as convert the duration from seconds to minutes 
tripdata$duration<-tripdata$duration/60
#check the pattern
ggplot(data=tripdata)+
  geom_boxplot(aes(y=duration))
#remove the outliers, top 0.1%
quantile(tripdata$duration,0.999)
tripdata<-tripdata[tripdata$duration<quantile(tripdata$duration,0.999),]

#sort the statiosn based on their latitude so that the stations are more close to each other in geography
stationdata<-StationData[order(StationData$lat,decreasing = T),]

#do a network analysis to observe number of trips between every 2 stations(can also be same station for staring and ending station) 
trip_count<-matrix(0,ncol=length(unique(tripdata$start_station_name)),nrow=length(unique(tripdata$end_station_name)))
rownames(trip_count)<-stationdata$name
colnames(trip_count)<-stationdata$name
for(i in 1:length(tripdata$id)){
  sta=tripdata[i,'start_station_name'][[1]]
  end=tripdata[i,'end_station_name'][[1]]
  trip_count[sta,end]=trip_count[sta,end]+1
}

b<-log(trip_count+1) #use log value to plot heatmap to view the relationship between stations
heatmap.2(b, Rowv=FALSE, symm=TRUE, margin=c(6, 6), trace="none")
#we can roughly observe a trip pattern from the heat map. where intra-city trips are commonly seen and inter-city trips seems to be rare
#hence, it is more useful to look at the data city by city when we study the bike problem

#calculate degree centrality of each station using trips data
#Next, we could calculate trips count starting and ending from each station, to calculate the in-degree and out-degree centrality of each node (station) in this network graph.
in_centrality<-as.data.frame(table(tripdata$start_station_name))
colnames(in_centrality)<-c('name','In_Degree_Centrality')
out_centrality<-as.data.frame(table(tripdata$end_station_name))
colnames(out_centrality)<-c('name','Out_Degree_Centrality')

#After that, the difference of [out degree] - [in degree] is calculated. By dividing the average of the two degree, we could get an index the severtiy of bike excess (diff<0) or bike shortage (diff>0) .
station_info<-full_join(in_centrality,out_centrality)
station_info<-full_join(stationdata,station_info)

#calculate the different between bikes in and out from each station, label as shortage or excess respectively 
station_info$Diff<-station_info$In_Degree_Centrality - station_info$Out_Degree_Centrality
station_info$Avg<-(station_info$In_Degree_Centrality + station_info$Out_Degree_Centrality) /2
station_info$index<- station_info$Diff / station_info$Avg
station_info$State<-ifelse(station_info$index>0,'Excess','Shortage')

if (!(file.exists("Data_station_info.csv"))) {
  write.csv(station_info, file = "Data_station_info.csv", row.names = FALSE)
}

ggmap(bay_area_map)+
  geom_point(data=station_info,aes(x=long,y=lat,color=State,size=abs(index)),alpha=0.5)+
  scale_size_continuous(guide = FALSE)+
  ggtitle('Bike Stations in Bay Area ')+
  theme_map()

pal <- colorFactor(c("blue", "red"), domain = c("Shortage", "Excess"),levels=c('Shortage','Excess'))
leaflet(station_info) %>% addTiles() %>%
  addCircleMarkers(lng=~long,lat=~lat,
                   radius = ~abs(index)*20,
                   color = ~pal(State), popup = ~name,
                   stroke = FALSE, fillOpacity = 0.5
  )
#We can then see that stations in SF are mostly facing shrtage issue as average bikes returning is less than bikes needed



#working on status9 dataset to view bike and dock availability 
#take an example of San Jose Caltrain Station
test_set<-Status9[1:5,]
leaflet() %>%  addTiles() %>%
  addMarkers(data = test_set, lng = ~long, lat = ~lat,
             popup = ~name)

PlotData<-Status9[(Status9$Date=='2014-05-02' & Status9$Hour=='12'& Status9$name=='San Jose Diridon Caltrain Station'),c(5,6,7,8,10,11) ]


#check bike availability
popup<-paste(sep='<br/>',
             PlotData$name, paste(sep=' ','Bike available:',PlotData$Average_Bikes),
             paste(sep=' ','Docks available:',PlotData$Average_Docks),
             paste(sep=' ','Total Docks here:',PlotData$dock_count)
)

leaflet() %>%  addTiles() %>%
  addMarkers(data=PlotData,lng = ~long, lat = ~lat,popup=popup
             ) #customer can view bike and dock availability from the map

#
San_Jose_Data<-Status9[(Status9$Date=='2014-05-02' & Status9$Hour=='12'& Status9$city=='San Jose'),c(5,6,7,8,10,11) ]
popup1<-paste(sep='<br/>',
              San_Jose_Data$name, paste(sep=' ','Bike available:',San_Jose_Data$Average_Bikes),
             paste(sep=' ','Docks available:',San_Jose_Data$Average_Docks),
             paste(sep=' ','Total Docks here:',San_Jose_Data$dock_count)
)
leaflet() %>%  addTiles() %>%
  addMarkers(data=San_Jose_Data,lng = ~long, lat = ~lat,popup=~popup1
  ) #plot all stations status at San Jose on 2014-05-02, and at 12 pm. 


##Part 3: Graphical Visualisation Analysis  

#number of stations by city
station_counts <- count(StationData, vars = city)
colnames(station_counts) <- c("City", "Number_of_Stations")
station_counts

#plotting number of stations by city
ggplot(station_counts, aes(x=City,y=Number_of_Stations)) + 
  geom_bar(aes(fill=City),stat="identity") + 
  ggtitle("Plot of number of Stations in a City") + ylab("Number of Stations")

#number of docks by city
dock_counts <- aggregate(StationData$dock_count, by=list(city=StationData$city), FUN=sum)
colnames(dock_counts) <- c("City", "Number_of_Docks")
dock_counts

#Plotting number of docks and stations by city
dock_station_counts <- left_join(station_counts,dock_counts, by = "City")
dock_station_counts <- dock_station_counts %>% gather(key, value, -City)
ggplot(dock_station_counts, aes(x = City, y = value)) + 
  geom_bar(aes(fill = key), stat="identity", position = "dodge") + 
  ggtitle("Plot of number of Docks and Stations in a City") +
  ylab("Number of Stations")

#Density plot of trip duration,for duration wintin 60 minutes 
ggplot(tripdata, aes(x = duration)) + 
  geom_density() + 
  xlim(0,60) +
  ggtitle("Density plot of trip duration")

#Density plots of trip duration by subscription type
subscription_trip <- tripdata[,c(2,10)]
ggplot(subscription_trip, aes(x = duration, fill = subscription_type)) + 
  geom_density(alpha=0.5) + 
  xlim(0,60) +
  ggtitle("Density plots of trip duration by subscription type")

#Adding date,month,hour,minute into trips data according to its start time

date.time<-t(as.data.frame(strsplit(tripdata$start_date,' ')))
row.names(date.time) = NULL

tripdata$date<-as.Date(date.time[,1],"%m/%d/%Y")
tripdata$time<-date.time[,2]

tripdata$Month<-format(tripdata$date,'%m')
tripdata$Month<-as.numeric(tripdata$Month)
# tripdata$Month <- mymonths[tripdata$Month]
tripdata$Month = factor(tripdata$Month, levels = month.name)

tripdata$Day <- weekdays(tripdata$date)
tripdata$Day<-factor(tripdata$Day, levels = c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"))

tripdata$hour<-ifelse(nchar(tripdata$time)==5,substr(tripdata$time,1,2),substr(tripdata$time,1,1))
tripdata$hour<-as.numeric(tripdata$hour)

#Counting trips by month
month_counts <- count(tripdata, vars = Month)
colnames(month_counts) <- c("Month","Number_of_Rides")
month_counts

#Plotting number of riders by month
ggplot(month_counts, aes(x=Month,y=Number_of_Rides)) + 
  geom_bar(stat="identity", fill="red") + ggtitle("Plot of number of rides by Month") + 
  ylab("Number of Rides")



#plotting by month and start city
StationData$count<-rownames(StationData)
start.city<-c()
for(i in 1:length(tripdata$id)){
  k<-which(tripdata$start_station_name[i] == unique(StationData$name))
  start.city[i]<-StationData$city[StationData$count==k]
  
}
tripdata$start.city<-start.city

end.city<-c()
for(i in 1:length(tripdata$id)){
  k<-which(tripdata$end_station_name[i] == unique(StationData$name))
  end.city[i]<-StationData$city[StationData$count==k]
  
}
tripdata$end.city<-end.city

tmp <- tapply(tripdata$id, INDEX = list(tripdata$Month, tripdata$start.city), length)
tmp <- as.data.frame(tmp) #dataframe coercion
tmp$Month = rownames(tmp) #Creating year column as the rownames
tmp

stats <- melt(tmp, id.vars = "Month", variable.name="series") 
stats$Month<-factor(stats$Month, levels = month.name)

#plotting variation in number of rides by month across the different cities
ggplot(stats, aes(x=Month,y=value)) + 
  geom_bar(stat="identity", aes(fill = series), position="fill") + 
  ylab("Proportion of City") + 
  scale_fill_manual("legend", values = c("Mountain View" = "black", "Palo Alto" = "brown", "Redwood City" = "red", "San Francisco"= "orange", "San Jose" = "yellow"))+
  theme(axis.text.x = element_text(angle = 90, hjust = 1))


#Counting trips by day
day_counts <- count(tripdata, vars = Day)
colnames(day_counts) <- c("Day","Number_of_Rides")
day_counts$Day<-factor(day_counts$Day, levels = c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"))

#Plotting number of riders by day
ggplot(day_counts, aes(x=Day,y=Number_of_Rides)) + geom_bar(stat="identity", fill="blue") + ggtitle("Plot of number of rides by Day") + ylab("Number of Rides")

tmp2 <- tapply(tripdata$id, INDEX = list(tripdata$Day, tripdata$start.city), length)
tmp2 <- as.data.frame(tmp2) #dataframe coercion
tmp2$Day = rownames(tmp2) #Creating year column as the rownames
tmp2

stats2 <- melt(tmp2, id.vars = "Day", variable.name="series") 
stats2$Day<-factor(stats2$Day, levels = c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"))

#plotting variation in number of rides by day across the different cities
ggplot(stats2, aes(x=Day,y=value)) + 
  geom_bar(stat="identity", aes(fill = series), position="fill") + 
  ylab("Proportion of City") + 
  scale_fill_manual("legend", values = c("Mountain View" = "black", "Palo Alto" = "brown", "Redwood City" = "red", "San Francisco"= "orange", "San Jose" = "yellow"))

#Counting trips by hour
hour_counts <- count(tripdata, vars = hour)
colnames(hour_counts) <- c("Hour","Number_of_Rides")

hour_counts$Hour<-factor(hour_counts$Hour,levels = seq(0,24))
#Plotting number of riders by day
ggplot(hour_counts, aes(x=Hour,y=Number_of_Rides)) + geom_bar(stat="identity", fill="green") + ggtitle("Plot of number of rides by Day") + ylab("Number of Rides")

tmp3 <- tapply(tripdata$id, INDEX = list(tripdata$hour, tripdata$start.city), length)
tmp3 <- as.data.frame(tmp3) #dataframe coercion
tmp3$Hour = rownames(tmp3) #Creating year column as the rownames
tmp3$Hour<-as.factor(tmp3$Hour)
tmp3

stats3 <- melt(tmp3, id.vars = "Hour", variable.name="series") 
stats3$Hour<-factor(stats3$Hour,levels = seq(0,24))
#plotting variation in number of rides by day across the different cities
ggplot(stats3, aes(x=Hour,y=value)) + geom_bar(stat="identity", aes(fill = series), position="fill") + ylab("Proportion of City") + scale_fill_manual("legend", values = c("Mountain View" = "black", "Palo Alto" = "brown", "Redwood City" = "red", "San Francisco"= "orange", "San Jose" = "yellow"))

if (!(file.exists("Data_cleaned_trip.csv"))) {
  write.csv(tripdata, file = "Data_cleaned_trip.csv", row.names = FALSE)
}



