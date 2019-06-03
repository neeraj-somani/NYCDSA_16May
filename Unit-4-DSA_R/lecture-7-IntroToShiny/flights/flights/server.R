library(shiny)
library(dplyr)
library(tidyr)
library(ggplot2)

flights <- read.csv(file = "./flights14.csv")

function(input, output) {
  output$delay <- renderPlot(
    flights %>%
      filter(origin == input$origin & dest == input$dest) %>%
      group_by(carrier) %>%
      summarise(departure = mean(dep_delay),
                arrival = mean(arr_delay)) %>% 
      gather(key = type, value = delay, -carrier) %>%
      ggplot(aes(x = carrier, y = delay, fill = type)) +
      geom_col(position = "dodge") + 
      ggtitle("Average delay")
  )
  
  output$count <- renderPlot(
    flights %>%
      filter(origin == input$origin & dest == input$dest) %>%
      group_by(carrier) %>%
      count() %>%
      ggplot(aes(x = carrier, y = n)) +
      geom_col(fill = "lightblue") +
      ggtitle("Number of flights")
  )
}

