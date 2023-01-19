################################################################################
#Company: Equilibre 
#Project: Shiny R app for cross-analysis of patient data between studies - MERCK
#Validation: None
#Program: study_comp_merck.R
#Source: NA
#Description: Create dashboard in shinyapps to compare EQU201 with similar Merck
#study
#Programmer: Frank Baring
#Reviewer: Nirajan Panthi
################################################################################

rm(list = ls())
status = "DEV"

if(TRUE){
  library("SciViews")
  library("xlsx")
  library("dplyr")
  library("PKNCA")
  library("tibble")
  library("openxlsx")
  library("naniar")
  library("berryFunctions")
  library("stringr")
  library("tidyr") 
  library("arsenal")
  library("lubridate")
  library("rapportools")
  library("readxl")
  library("ggplot2")
  library("equivalenceTest")
  library("readr")
  library("TOSTER")
  library("ggpmisc")
  library("haven")
  library("imager")
  library("datasets")
  library("shiny")
  library("shinythemes")
  library("dplyr")
  library("DT")
  library("ggplot2")
  library("forcats")
  library("car")
  library("nortest")
  library("tseries")
  library("RcmdrMisc")
  library("lmtest")
}# Load packages

#Mend rounding function
round.off <- function (x, digits=0) 
{
  posneg = sign(x)
  z = trunc(abs(x) * 10 ^ (digits + 1)) / 10
  z = floor(z * posneg + 0.5) / 10 ^ digits
  return(z)
}

# Load Data---------------------------------------------------------------------
EQU.data.PP <- read_xpt('ADPP.xpt') %>% 
  filter(TRTACAT == 'SAD') %>%
  select('USUBJID','TRTACAT','ATRT','ATPT',
         'PPSCAT','PARAMCD','AVAL')
EQU.data.PC <- read_xpt('ADPC.xpt') %>%
  filter(TRTACAT == 'SAD', PARAMCD == 'IVERM') %>%
  select('USUBJID','TRTACAT','ATRT',
         'AVISIT','ATPTN','PARAMCD','AVAL')
MERCK.data <- read.xlsx("MERCK_DATA.xlsx")
MERCK.30mg <- load.image("MERCK_30mg_cohort.png")

# Manipulate Data---------------------------------------------------------------
# PP data
EQU.data.Cmax <- EQU.data.PP %>% filter(PARAMCD == 'CMAX')
EQU.data.Tmax <- EQU.data.PP %>% filter(PARAMCD == 'TMAX')

datuse.EQU.Cmax <- (EQU.data.Cmax %>% group_by(ATRT) %>% 
                      summarise(MEAN = mean(as.numeric(AVAL)),
                                SD = sd(as.numeric(AVAL))))[c(1,3,5,4,6,2),]
datuse.EQU.Tmax <- (EQU.data.Tmax %>% group_by(ATRT) %>%
                      summarise(MEAN = mean(as.numeric(AVAL)),
                                SD = sd(as.numeric(AVAL))))[c(1,3,5,4,6,2),]

datuse.EQU.Cmax$ATRT <- c("10mg (fasted) - Day 1","20mg (fasted) - Day 1",
                          "40mg (fed) - Day 1", "40mg (fasted) - Day 1",
                          "80mg (fasted) - Day 1","120mg (fasted) - Day 1")
datuse.EQU.Tmax$ATRT <- c("10mg (fasted) - Day 1","20mg (fasted) - Day 1",
                          "40mg (fed) - Day 1", "40mg (fasted) - Day 1",
                          "80mg (fasted) - Day 1","120mg (fasted) - Day 1")

EQU.fasted.Cmax <- datuse.EQU.Cmax %>% 
                       filter(grepl("fasted",ATRT)) %>% 
                          mutate(ATRT = parse_number(ATRT))
EQU.fasted.Tmax <- datuse.EQU.Tmax %>% 
                       filter(grepl("fasted",ATRT)) %>% 
                          mutate(ATRT = parse_number(ATRT))
MERCK.fasted <- MERCK.data %>% 
                       filter(grepl("fasted",DOSE),grepl("Day 1",DOSE)) %>% 
                                              mutate(DOSE = parse_number(DOSE))
combined.fasted.Cmax <- rbind(EQU.fasted.Cmax %>% 
                          mutate(DOSE = ATRT, Cmax = MEAN,STUDY = "EQU") %>% 
                              select(DOSE,Cmax,STUDY),MERCK.fasted %>% 
                                  select(DOSE,Cmax) %>% mutate(STUDY = "MERCK"))
combined.fasted.Tmax <- rbind(EQU.fasted.Tmax %>% 
                          mutate(DOSE = ATRT, Tmax = MEAN,STUDY = "EQU") %>% 
                                      select(DOSE,Tmax,STUDY), MERCK.fasted %>% 
                                  select(DOSE,Tmax) %>% mutate(STUDY = "MERCK"))
combined.fasted <- rbind(combined.fasted.Cmax %>% 
                    mutate(VAL = Cmax,PARA = "Cmax") %>% 
                        select(STUDY,DOSE,PARA,VAL),combined.fasted.Tmax %>% 
                                          mutate(VAL = Tmax,PARA = "Tmax") %>% 
                                                    select(STUDY, DOSE,PARA,VAL))

# PC data
EQU.co_2.conc <- EQU.data.PC %>%
          filter(ATRT == 'SAD EQU-001 40 mg',!grepl('Food Effect',AVISIT)) %>% 
            group_by(ATPTN, AVISIT) %>% summarise(MEAN_CONC = mean(AVAL),.groups = 'drop') %>%
                            mutate(DOSE = "SAD EQU-001 40 mg") %>% relocate(DOSE,.before = ATPTN)

EQU.co_3.conc <- EQU.data.PC %>%
          filter(ATRT == 'SAD EQU-001 80 mg') %>% group_by(ATPTN, AVISIT) %>%
                        summarise(MEAN_CONC = mean(AVAL),.groups = 'drop') %>%
                                         mutate(DOSE = "SAD EQU-001 80 mg") %>% 
                                                  relocate(DOSE,.before = ATPTN)

#AUC Values---------------------------------------------------------------------
co_2_auc_48 <- EQU.data.PC %>% 
  filter(ATRT == 'SAD EQU-001 40 mg',!grepl('Food Effect',AVISIT),ATPTN <= 48.0) %>%
                      select(USUBJID,ATRT,AVISIT,ATPTN,AVAL) %>% group_by(USUBJID)%>%
                        mutate(auc = pk.calc.auc(conc = AVAL ,time = ATPTN,interval= c(0,48)))%>%
                                                     select(USUBJID, auc)%>%unique()%>%ungroup()%>% 
                                                        summarise(geometric_mean = exp(mean(log(auc))))

co_2_auc_72 <- EQU.data.PC %>% 
  filter(ATRT == 'SAD EQU-001 40 mg',!grepl('Food Effect',AVISIT),ATPTN <= 72.0) %>%
                       select(USUBJID,ATRT,AVISIT,ATPTN,AVAL) %>% group_by(USUBJID)%>%
                         mutate(auc = pk.calc.auc(conc = AVAL ,time = ATPTN,interval= c(0,72)))%>%
                                                      select(USUBJID, auc)%>%unique()%>%ungroup()%>% 
                                                        summarise(geometric_mean = exp(mean(log(auc))))

co_3_auc_48 <- EQU.data.PC %>% 
  filter(ATRT == 'SAD EQU-001 80 mg',ATPTN <= 48.0) %>%
                        select(USUBJID,ATRT,AVISIT,ATPTN,AVAL) %>% group_by(USUBJID)%>%
                          mutate(auc = pk.calc.auc(conc = AVAL ,time = ATPTN,interval= c(0,48)))%>%
                                                      select(USUBJID, auc)%>%unique()%>%ungroup()%>% 
                                                        summarise(geometric_mean = exp(mean(log(auc))))

co_3_auc_72 <- EQU.data.PC %>% 
  filter(ATRT == 'SAD EQU-001 80 mg',ATPTN <= 72.0) %>%
                       select(USUBJID,ATRT,AVISIT,ATPTN,AVAL) %>% group_by(USUBJID)%>%
                         mutate(auc = pk.calc.auc(conc = AVAL ,time = ATPTN,interval= c(0,72)))%>%
                                                      select(USUBJID, auc)%>%unique()%>%ungroup()%>% 
                                                        summarise(geometric_mean = exp(mean(log(auc))))

#EQU AUC data frame
EQU.AUC.df <- data.frame(DOSE = c(rep("SAD EQU-001 40 mg",2),rep("SAD EQU-001 80 mg",2)),
                                                    VAR = rep(c("AUC 0-48","AUC 0-72"),2),
                                                      VAL = c(co_2_auc_48[[1]],co_2_auc_72[[1]],
                                                              co_3_auc_48[[1]],co_3_auc_72[[1]]))



#SHINY R APPLICATION############################################################
# UI page
ui <- fluidPage(
  fluidRow(
    style = "border-width: 2px; border-style: solid; border-color: black;",
    h1("Cmax/Tmax Comparison"),
    sidebarLayout(
      sidebarPanel(
        radioButtons("regInput", "Regression line:",
                    choices = c("NO", "YES"),
                          selected = "NO"),
        selectInput("paramInput", "Parameter:",
                    choices = c("Cmax", "Tmax"))
      ),
      mainPanel(
          column(
            11,
            plotOutput("C_T_plot"),
            dataTableOutput("C_T_table",width = 20)
          )
         )
        )
      ),
    fluidRow(
      style = "border-width: 2px; border-style: solid; border-color: black;",
      h1("AUC Comparison"),
      column(5,
        h3("Equilibre"),
        dataTableOutput("EQU_auc_table"),
        h3("Merck"),
        dataTableOutput("MERCK_auc_table")
      ),
      column(7,
        h2("Concentration over time: EQU 40mg and 80mg cohorts"),
        plotOutput("EQU_conc_plot"),
        h2("Concentration over time: MERCK 30mg and 60mg cohorts"),
        tags$img(src='MERCK_Day1_Day7.png')
      )
   )
)


# Define a server for the Shiny app
server <- function(input, output, session) {
  
# Plots-------------------------------------------------------------------------
  
  # EQU + MERCK Cmax/Tmax data plot
  output$C_T_plot <- renderPlot({
    
    filtered <- combined.fasted %>% filter(PARA == input$paramInput)
    
    # Plot
    p <- ggplot(data = filtered, aes(x = DOSE, y = VAL)) +
       geom_point(aes(color = STUDY),size = 3) +
       xlab("Dose, mg")
    # Conditional Y-axis label
    if(input$paramInput == "Cmax")
      p <- p+ylab(paste(input$paramInput,", ng/mL",sep= ""))
    else if(input$paramInput == "Tmax")
      p <- p+ylab(paste(input$paramInput,", hr", sep = ""))
    # Conditional regression line inclusion
    if(input$regInput == "YES"){
      p <- p+
           geom_smooth(aes(color = STUDY),method = 'lm', formula = y~x,se = F) +
           stat_poly_eq(aes(color = STUDY,label = paste(after_stat(eq.label),
                              after_stat(rr.label), sep = "*\", \"*")),size = 6)
    }
    p
  })
  
  # EQU concentration plot for cohorts 2 and 3
  output$EQU_conc_plot <- renderPlot({
    
    datuse <- rbind(EQU.co_2.conc,EQU.co_3.conc)
    
    # Plot
    p <- ggplot(data = datuse, aes(x = ATPTN, y = MEAN_CONC)) +
      geom_point(aes(color = DOSE),size = 3) +
      xlab("Timepoint (hr)")+
      ylab("Concentration (ng/mL)")+
      theme(text = element_text(size = 20))+
      geom_line(aes(color = DOSE))+
      geom_point(aes(color = DOSE))
    p
  })
  
# Tables------------------------------------------------------------------------
  
  # EQU + MERCK Cmax/Tmax data table
  output$C_T_table <- renderDataTable({
    
    filtered <- combined.fasted %>% filter(PARA == input$paramInput)
    
    # Table
    t <- filtered %>%
           mutate(DOSE = paste(DOSE,"mg",sep=''),VAL = round.off(VAL,digits = 2)) %>% 
                                                                select(STUDY,DOSE,VAL)
    if(input$paramInput == "Cmax")
      names(t)[which(names(t) == "VAL")] <- paste(input$paramInput,", ng/mL",sep= "")
    else if(input$paramInput == "Tmax")
      names(t)[which(names(t) == "VAL")] <- paste(input$paramInput,", hr", sep = "")
    t
    
  },
  options=list(paging=F,
               info=F,
               ordering=F,
               columns.name=F,
               bLengthChange=0,
               bFilter=0,                                    
               bInfo=0,                                     
               bAutoWidth=0)
  )
  
  #EQU AUC table
  output$EQU_auc_table <- renderDataTable({
    
    # Table
    t <- EQU.AUC.df %>% mutate(VAL = round.off(VAL,digits = 2))
    t
  },
  options=list(paging=F,
               info=F,
               ordering=F,
               columns.name=F,
               bLengthChange=0,
               bFilter=0,                                    
               bInfo=0,                                     
               bAutoWidth=0)
  )
  
  #MERCK AUC table
  output$MERCK_auc_table <- renderDataTable({
    
    #Table
    t <- MERCK.data %>% filter(!is.na(`AUC(0-60)`)) %>%
                                mutate(VAL = `AUC(0-60)`, VAR = "AUC(0-60)")%>%
                                                            select(DOSE,VAR,VAL)
    t
  },
  options=list(paging=F,
               info=F,
               ordering=F,
               columns.name=F,
               bLengthChange=0,
               bFilter=0,                                    
               bInfo=0,                                     
               bAutoWidth=0)
  )
  
}


# Run app
shinyApp(ui = ui, server = server)
