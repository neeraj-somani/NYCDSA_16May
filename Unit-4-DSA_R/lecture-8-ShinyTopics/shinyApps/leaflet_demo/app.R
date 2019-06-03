library(googleVis)
library(leaflet)
library(shiny)
library(maps)

colStates <- map("state", fill = TRUE, plot = FALSE,
                 region = c("florida", "louisiana", "mississippi", 
                            "alabama", "georgia", "tennesse"))

ui <- fluidPage(
  leafletOutput("mymap"),
  br(),
  checkboxInput("show", "Show States", value = FALSE)
)

server <- function(input, output, session) {
  output$mymap <- renderLeaflet({
    leaflet(Andrew) %>%
      addProviderTiles("Esri.WorldStreetMap") %>%
      addPolylines(~Long, ~Lat)
  })
  observeEvent(input$show, {
    proxy <- leafletProxy("mymap")
    if(input$show) {
      proxy %>% addPolygons(data=colStates, stroke = FALSE,
                            fillColor = heat.colors(6, alpha = 1),
                            
                            layerId = LETTERS[1:6])
    } else {
      proxy %>% removeShape(layerId = LETTERS[1:6])
    }
  })
}
shinyApp(ui, server)