library(shiny)
library(dplyr)
library(tidyr)
library(ggplot2)

function(input, output, session) {
  
  observe({
    dest <- unique(flights %>%
                     filter(flights$origin == input$origin) %>%
                     .$dest)
    updateSelectizeInput(
      session, "dest",
      choices = dest,
      selected = dest[1])
  })
  
  flights_delay <- reactive({
    flights %>%
      filter(origin == input$origin & dest == input$dest) %>%
      group_by(carrier) %>%
      summarise(n = n(),
                departure = mean(dep_delay),
                arrival = mean(arr_delay))
  })

  output$delay <- renderPlot(
    flights_delay() %>%
      gather(key = type, value = delay, departure, arrival) %>%
      ggplot(aes(x = carrier, y = delay, fill = type)) +
      geom_col(position = "dodge") +
      ggtitle("Average delay")
  )

  output$count <- renderPlot(
    flights_delay() %>%
      ggplot(aes(x = carrier, y = n)) +
      geom_col(fill = "lightblue") +
      ggtitle("Number of flights")
  )
}