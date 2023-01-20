################################################################################
#Company: Equilibre 
#Project: EQU201 -- Seizure tracking data table build
#Validation: Peer-review
#Program: EQU-201_tracking_script.R
#Source: NA
#Basedir: ~/Documents/EQU-001/EQU-201/subject_seizure_count/
#Description: Create data book for tracking subject seizures in EQU201 study
#Input: [Basedir]/exports/[DATE FILE]/data/
#Output: [Basedir]/exports/[DATE FILE]/output/
#Programmer: Frank Baring
#Reviewer: Nirajan Panthi
################################################################################

rm(list = ls())
status = "DEV"

#Set head working directory to correct folder
setwd("C:/Users/FrankBaring/OneDrive - Equilibre/Documents/EQU-001/EQU-201/subject_seizure_count")

#Function libraries
source("./functions/EQU201_seizure_tracking_script[FUNC].R")

#Mend rounding function
round.off <- function (x, digits=0) 
{
  posneg = sign(x)
  z = trunc(abs(x) * 10 ^ (digits + 1)) / 10
  z = floor(z * posneg + 0.5) / 10 ^ digits
  return(z)
}

if(TRUE){#Load packages
  library("xlsx")
  library("shiny")
  library("dplyr")
  library("M3")
  library("tibble")
  library("scales")
  library("openxlsx")
  library("naniar")
  library("splines")
  library("berryFunctions")
  library("stringr")
  library("tidyr") 
  library("arsenal")
  library("lubridate")
  library("rapportools")
  library("readxl")
  library("ggplot2")
  library("equivalenceTest")
  library("TOSTER")
  library("extraoperators")
}#Load packages

#Start time and set base directory [CHANGE EACH WEEK]
t1 <- Sys.time()
setwd("./exports/06-24-2022")

if(TRUE){
#Pull data of each subject into data frames-------------------------------------
#Import data
EOS <- read.csv("./data/DS.csv") %>% 
                                    select(SUBID,SUBNUM,DSEXDT,DSOPNEX,DSOTHCOM)
cohort_df <- read.csv("./data/RAND.csv") %>% select(SUBNUM,COHORT)
SZL <- read.csv("./data/SZL.csv")
subject_list <- read.xlsx("./data/subject_list.xlsx")
#Data restructuring
EOS <- df_date(EOS,colnum = 3,my_option = 1)
subject_list <- df_cut(subject_list)
df_names <- subject_list[[3]]
cohort_df <- rbind(cohort_df, data.frame('SUBNUM' = 
                subject_list[which(subject_list$Subject %!in%
                               cohort_df$SUBNUM),'Subject']) %>% 
                                    mutate(COHORT = 'not randomized'))
names(cohort_df) <- c("SUBID", "cohort")
SZL <- df_date(SZL,colnum = 14,my_option = 1)
df_list <- lapply(1:nrow(subject_list),df_listing) %>% df_rename()
for(i in 1:length(df_list)){
  df_list[[i]] <- df_remove_duplicates(df_list[[i]],2)
  df_list[[i]] <- df_list[[i]][order(df_list[[i]][,2]),]
}
df_list <- df_med_check(df_list)[[1]]
datset_errors <- df_med_check(df_list)[[2]]
df_list_overall <- df_list
df_list <- df_split_OLE(df_list_overall,EOS,fragment = 1)
df_list_OLE <- df_split_OLE(df_list_overall,EOS,fragment = 2)
OLE_keep <- subject_list[which(grepl("OLE",subject_list[,4]) == T),3]
df_list_OLE <- df_list_OLE[which(names(df_list_OLE) %in% OLE_keep)]
df_list_base <- df_split_trt(df_list,1)
df_list_trt <- df_split_trt(df_list,2)
}#Data preparation


if(TRUE){
#Create summary data frame based on the file list-------------------------------
#TRT----------------------------------------------------------------------------
df_sum <- cbind(data.frame(cohort = rep(NA,nrow(subject_list))),
                                           screening_num = subject_list[,3]) %>% 
           mutate(total_seizures_at_baseline = NA, number_of_baseline_days = NA,
                 seizures_per_day_BASE = NA, total_seizures_with_treatment = NA,
                       number_of_treatment_days = NA, seizures_per_day_TRT = NA,
            percentage_change = NA, change_comment = NA, completion_status = NA)
#Fill cohort column
for(i in 1:nrow(df_sum)){
  df_sum[i,'cohort'] <- cohort_df %>%
                            filter(SUBID == df_sum[i,"screening_num"]) %>% 
                                                                  select(cohort)
}
#Fill completion status column
df_sum <- df_completion_status(df_sum, subject_list,EOS)
#Set correct column types
for(i in 1:length(df_list)){
  df_list[[i]][,4] <- sapply(df_list[[i]][,4], as.numeric)
}
#Fill baseline seizure count column
df_sum$total_seizures_at_baseline <- lapply(1:nrow(df_sum), df_colsum_base)
df_sum <- transform(df_sum, total_seizures_at_baseline = 
                                         as.numeric(total_seizures_at_baseline))
#Fill number of baseline days column
df_sum$number_of_baseline_days <- lapply(1:nrow(df_sum), df_daycount_base)
df_sum <- transform(df_sum, number_of_baseline_days = 
                                            as.numeric(number_of_baseline_days))
#Fill seizure per day at baseline column
for(i in 1:nrow(df_sum)){
  if(df_sum[i,'total_seizures_at_baseline'] != 0){
     df_sum[i,'seizures_per_day_BASE'] <- round.off(as.integer(df_sum[i,'total_seizures_at_baseline'])/
                                           as.integer(df_sum[i,'number_of_baseline_days']),digits = 2)
  }
}
#Fill treatment seizure count column
df_sum$total_seizures_with_treatment <- lapply(1:nrow(df_sum), df_colsum_trt)
df_sum <- transform(df_sum, total_seizures_with_treatment = 
                                      as.numeric(total_seizures_with_treatment))
#Fill number of treatment days column
df_sum$number_of_treatment_days <- lapply(1:nrow(df_sum), df_daycount_trt)
df_sum <- transform(df_sum, number_of_treatment_days = 
                                           as.numeric(number_of_treatment_days))
#Fill seizures per day with treatment column
for(i in 1:nrow(df_sum)){
  if(df_sum[i,'total_seizures_with_treatment'] != 0){
    df_sum[i,'seizures_per_day_TRT'] <- round.off(as.integer(df_sum[i,'total_seizures_with_treatment'])/
                                            as.integer(df_sum[i,'number_of_treatment_days']),digits = 2)
  }
}
#Fill percentage change column
df_sum <- df_perc_change(df_sum)
#Fill change comment column
df_sum <- df_perc_change_comments(df_sum)
#Reorder data frame
df_sum <- df_sum %>% arrange(factor(screening_num, levels = as.vector(cohort_df$SUBID)))
#4 week view--------------------------------------------------------------------
#Make baseline data frame
df_monthly_base <- data.frame(screening_num = names(df_list))
df_monthly_base <- df_4week_coladd(df_monthly_base,df_list,'BASELINE')
#Make treatment data frame
df_monthly_trt <- data.frame(screening_num = names(df_list))
df_monthly_trt <- df_4week_coladd(df_monthly_trt,df_list_trt,'TREATMENT')
#Make OLE data frame
df_monthly_OLE <- data.frame(screening_num = names(df_list))
df_monthly_OLE <- df_4week_coladd_OLE(df = df_monthly_OLE,df_list = df_list_OLE)
#Fill data frame
df_monthly <- cbind(df_4week(df_monthly_base,df_list_base),
                    df_4week(df_monthly_trt,df_list_trt)[,2:ncol(df_monthly_trt)],
                    df_4week_OLE(df_monthly_OLE,df_list_OLE)[,2:ncol(df_monthly_OLE)])
#Reorder data frame
df_monthly <- df_monthly %>% 
                arrange(factor(screening_num, levels = as.vector(cohort_df$SUBID))) %>%
                  mutate("Overall seizures per 28 days in BASELINE" = NA, cohort = NA) %>%
                    relocate(`Overall seizures per 28 days in BASELINE`,.after = 
                                        max(which(grepl("BASELINE",names(df_monthly))))) %>%
                      relocate(cohort,.before = screening_num)
#Insert overall seizures per 28 days for baseline
for(i in 1:nrow(df_monthly)){
  df_monthly[i,'cohort'] <- cohort_df %>%
                              filter(SUBID == df_monthly[i,"screening_num"]) %>% 
                                                                  select(cohort)
  j <- which(names(df_list_base) == df_monthly[i,'screening_num'])
  df_monthly[i,"Overall seizures per 28 days in BASELINE"] <- 
    round.off((sum(df_list_base[[j]][4])/nrow(df_list_base[[j]]))*28,digits = 2)
}
#OLE----------------------------------------------------------------------------
#Input subject numbers
df_sum_OLE <- data.frame(cohort = rep(NA,length(df_list_OLE)),
                                         screening_num = names(df_list_OLE)) %>% 
                   mutate(seizures_per_day_BASE = NA, seizures_per_day_TRT = NA, 
                            total_seizures_in_OLE = NA, number_of_OLE_days = NA, 
                        seizures_per_day_OLE = NA, '%change_from_baseline' = NA)
#Fill cohort column
for(i in 1:nrow(df_sum_OLE)){
  df_sum_OLE[i,'cohort'] <- cohort_df %>%
                             filter(SUBID == df_sum_OLE[i,"screening_num"]) %>%
                                                                  select(cohort)
}
#Correct column types
for(i in 1:length(df_list_OLE)){
  if(typeof(df_list_OLE[[i]]) != 'logical'){
    df_list_OLE[[i]][,4] <- sapply(df_list_OLE[[i]][,4], as.numeric)
  }
}
#Fill OLE columns
for(i in 1:nrow(df_sum_OLE)){
  #Pull data from df_sum
  tmp <- which(names(df_list_OLE) == df_sum_OLE[i,'screening_num'])
  df_sum_OLE[i,'seizures_per_day_BASE'] <- df_sum %>%
                      filter(screening_num == df_sum_OLE[i,'screening_num']) %>%
                                                   select(seizures_per_day_BASE)
  df_sum_OLE[i,'seizures_per_day_TRT'] <- df_sum %>%
                      filter(screening_num == df_sum_OLE[i,'screening_num']) %>%
                                                    select(seizures_per_day_TRT)
  #Add OLE data
  if(typeof(df_list_OLE[[tmp]]) != 'logical'){
    df_sum_OLE[i,'total_seizures_in_OLE'] <- df_colsum_OLE(tmp)
    df_sum_OLE[i,'number_of_OLE_days'] <- nrow(df_list_OLE[[tmp]])
    df_sum_OLE[i,'seizures_per_day_OLE'] <- round.off(df_sum_OLE[i,'total_seizures_in_OLE']/
                                                df_sum_OLE[i,'number_of_OLE_days'],digits = 2)
    df_sum_OLE[i,'%change_from_baseline'] <- round.off(((df_sum_OLE[i,'seizures_per_day_OLE']/
                                  df_sum_OLE[i,'seizures_per_day_BASE']) - 1)*100, digits = 2)
  }
}
#Reorder data frame
df_sum_OLE <- df_sum_OLE %>% arrange(factor(screening_num, levels = as.vector(cohort_df$SUBID)))
}#Data sets


if(TRUE){
#Print plots
pre_tr_df <- df_plots(df_list)
df_plots_OLE(df_list_OLE)
}#Plots


if(TRUE){
#EDC data set errors
for(i in 1:length(datset_errors)){cat(datset_errors[[i]][1],'\n')}
#Time elapsed
t2 <- Sys.time()
time_elapsed <- t2 - t1
cat('-----------------------------------------\n')
cat("Time elapsed: ",as.numeric(time_elapsed),"\n")
}#Program outputs
################################################################################


if(TRUE){
setwd("./output")
#Free memory
rm(list=ls()[!ls()%in%c("df_sum","df_monthly","df_sum_OLE")])
#Write summary table and baseline average table to excel spreadsheet
my_date <- str_replace_all(Sys.Date(), "-", "_")
sheets <- list("Summary" = df_sum, "4-Week View" = df_monthly, "OLE" = df_sum_OLE)
write.xlsx(sheets, file = paste(my_date,"EQU201_report.xlsx"),
            col.names = TRUE, row.names = FALSE, append = FALSE, showNA = FALSE)
setwd("..")
}#Export


