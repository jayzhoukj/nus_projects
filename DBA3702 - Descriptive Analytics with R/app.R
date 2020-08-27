#app.R
library(shiny)
library(leaflet)
library(leaflet.extras)
library(shinyTime)
library(dplyr)
library(readr)
library(shinythemes)
library(ggmap)
library(ggthemes)

# global data
Data_cleaned <- read_csv('Data_cleaned.csv')
data <- Data_cleaned[order(Data_cleaned$name),]
data1 <- data %>%
group_by(Date, Year, Hour, name, lat, long, dock_count, city) %>%
summarize(Average_Bikes= mean(Average_Bikes), Average_Docks =mean(Average_Docks))
data2<-read_csv('Data_cleaned_trip.csv')
data3<-read_csv('Data_station_info.csv')

shinyApp(
  ui = tagList(
    shinythemes::themeSelector(),
    navbarPage(
      "MOFO BIKE",
      tabPanel("Distribution of bikes",
               sidebarPanel(
                 textInput("txt", "How shall we address you?", ""),
                 
                 #date input
                 dateInput("date",
                           label = "Select a Date",
                           value = min(data1$Date),
                           min = min(data1$Date),
                           max= max(data1$Date)
                 ),
                 #Hour input  
                 numericInput("hour", 
                              label = "Select the Hour",
                              value = min(data1$Hour),
                              min = min(data1$Hour),
                              max = max(data1$Hour)
                 ),
                 #City Input
                 checkboxGroupInput("cities",
                                    label = "Select a City",
                                    selected = unique(data1$city)[1],
                                    choices = unique(data1$city),
                                    inline = F),
                 #Station Input
                 selectInput("stations",
                             label = "Select a Bike Station",
                             choices = '',
                             multiple = T
                 ),
                
                 width = 3
               ),
               mainPanel(verbatimTextOutput(("txtout")),
                 leafletOutput(outputId = "plotMap")
               )
      ),
      
      tabPanel("Explore your trip",
               sidebarPanel(
                 
                 selectInput("citi",
                             label = "Which city are you in?",
                             choices = c(unique(data1$city))
                 ),
                 
                 
                 #Start station Input
                 selectInput("start",
                             label = "Start Station",
                             choices = c(unique(data1$name))
                 ),
                 
                 
                 #End station Input
                 selectInput("end",
                             label = "End Station",
                             choices = c(unique(data1$name))
                 ),
                 
                 radioButtons(inputId = "mapType",label="Map Type",
                              choices = c("roadmap","satellite","terrain","hybrid",
                                          "toner","toner-lite","terrain-background","watercolor"))
                 
                 
                 
                 
                 
                 
                 
                 
                 
               ),
               mainPanel(verbatimTextOutput("text"),
                         plotOutput("plotStationState")
               )
               
               
      ),
    
      
      tabPanel("Customer Trip Pattern", 
               sidebarPanel(
                 #By Input
                 selectInput("By",
                             label = "By",
                             choices = c("Month",'Day','Hour')
                 ),
                 #City Input
                 selectInput("city",
                                    label = "Select City",
                                    choices = unique(data1$city)
                                    )
                 
               
               
               ),
               mainPanel(
                 plotOutput("distPlot")))
      
      
      
      
    
               
      
      
        
      
    
    )
    ),

      
server <- function(session,input, output){
        output$txtout <- renderText({
          paste('Hi,',input$txt,'.','Looking for a bike?')
        })
  
  
        #event such that only stations in the chosen cities are returned
        observeEvent(
          input$cities,
          updateSelectInput(session, 
                            "stations",
                            label = "Station Input",
                            choices = unique(data1$name[data1$city %in% input$cities]),
                            selected = unique(data1$name[data1$city %in% input$cities])[1]
          ))
        
        
        #function for leaflet plot
        dpoints <- function(){
          data1[(data1$Date==input$date & 
                   data1$Hour==input$hour & 
                   (data1$name %in% input$stations)
          ), ]
        }
        #for leaflet plot
        output$plotMap <- renderLeaflet({
          b <- dpoints()
          popups <- paste(sep='<br/>',
                          input$stations, paste(sep=' ','Bikes available:',b$Average_Bikes),
                          paste(sep=' ','Docks available:',b$Average_Docks),
                          paste(sep=' ','Total Docks here:',b$dock_count))
          print(b)
          leaflet() %>% addTiles() %>%
            addMarkers(data = b,
                       lng = ~long,
                       lat = ~lat,
                       popup = popups,
                       clusterOptions = markerClusterOptions()
            )
        }
        )
        
        get.graphical.data<-function(){
          city<-input$city
          data<-data2[data2$start.city==city,c('id','hour','Month','Day')]
          data
        }  
        month.count<-function(){
          data<-get.graphical.data()
          month_counts <- count(data, vars = Month)
          colnames(month_counts) <- c("Month","Number_of_Rides")
          mymonths <- c("January","February","March",
                        "April","May","June",
                        "July","August","September",
                        "October","November","December")
          month_counts$Month<-factor(month_counts$Month,levels=mymonths)
          month_counts
        }
        
        day.count<-function(){
          data<-get.graphical.data()
          day_counts <- count(data, vars = Day)
          colnames(day_counts) <- c("Day","Number_of_Rides")
          day_counts$Day<-factor(day_counts$Day, levels = c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"))
          day_counts
        }
        
        hour.count<-function(){
          data<-get.graphical.data()
          hour_counts <- count(data, vars = hour)
          colnames(hour_counts) <- c("Hour","Number_of_Rides")
          hour_counts$Hour<-factor(hour_counts$Hour,levels = seq(0,24))
          hour_counts
        }
        
        output$distPlot<-renderPlot({
          if(input$By=='Month'){
            ggplot(data=month.count(), aes(x=Month,y=Number_of_Rides)) + 
            geom_bar(stat="identity", fill="red") + ggtitle("Plot of number of rides by Month") + 
            ylab("Number of Rides")+
            theme(axis.text.x = element_text(angle = 90, hjust = 1))
          }
          else if(input$By=='Day'){
            ggplot(data=day.count(), aes(x=Day,y=Number_of_Rides)) + 
              geom_bar(stat="identity", fill="blue") + 
              ggtitle("Plot of number of rides by Day") + ylab("Number of Rides")
          }
          else{
            ggplot(data=hour.count(), aes(x=Hour,y=Number_of_Rides)) + 
              geom_bar(stat="identity", fill="green") + 
              ggtitle("Plot of number of rides by Day")
          }
        })
        
        
          get.trip.count<-function(){
            df_trip<-data2[(data2$start_station_name==input$start & data2$end_station_name==input$end),
                           c('id','start_station_name','end_station_name')]
            df_trip
          }
          
          count.trip<-function(){
            trip_count<-matrix(0,ncol=length(unique(get.trip.count()$start_station_name)),nrow=length(unique(get.trip.count()$end_station_name)))
            rownames(trip_count)<-input$start
            colnames(trip_count)<-input$end
            for(i in 1:length(get.trip.count()$id)){
              sta=get.trip.count()[i,'start_station_name'][[1]]
              end=get.trip.count()[i,'end_station_name'][[1]]
              trip_count[sta,end]=trip_count[sta,end]+1
            }
            trip_count
          }
          
          
          observeEvent(
            input$citi,
            updateSelectInput(session, 
                              "start",
                              label = "Start Station Input",
                              choices = unique(data1$name[data1$city %in% input$citi]),
                              selected = unique(data1$name[data1$city %in% input$citi])[1]
            ))
          
          observeEvent(
            input$citi,
            updateSelectInput(session, 
                              "end",
                              label = "End Station Input",
                              choices = unique(data1$name[data1$city %in% input$citi]),
                              selected = unique(data1$name[data1$city %in% input$citi])[1]
            ))
          
          output$text <- renderText({
            paste('Number of trips with same route:',count.trip(),sep=' ')
          
          })
          
          register_google(key='AIzaSyBKNZLfGl7FCDNmIhZmibexeWPBKl5XWXI')
          
          getMap <- reactive({
            get_map(as.character(input$citi), zoom = 13, maptype = input$mapType)}
          )
          
            
            
          output$plotStationState <-renderPlot({
            ggmap(getMap())+
              geom_point(data=data3,aes(x=long,y=lat,color=State,size=abs(index)),alpha=0.5)+
              scale_size_continuous(guide = FALSE)+
              ggtitle(paste('Bike Stations infomation'))+
              theme_map()
          })
          
          
        
        
    
      }
      
)
      

