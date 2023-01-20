#Functions for EQU-201 subject seizure tracking, using EDC exports

#Function to remove duplicates in given column
df_remove_duplicates <- function(df,colnum){
  datuse <- df[!duplicated(df[,colnum]),]
  return(datuse) 
}  

#Function to iterate through a list of data frames and change formate of date column
df_date <- function(df,colnum,my_option){
  if(my_option == 1){
  df[,colnum] <- as.Date(df[[colnum]],format = '%Y-%m-%d')
  }else if(my_option == 2){
  df[,colnum] <- as.Date(df[[colnum]],format = '%d-%b-%Y')
  }
  return(df)
}

#Function to rename data frames to a specific string(subject number in this case) 
#within the tibble
df_rename <- function(my_list){
  #Vector of list indexes to be removed
  tb_rm <- vector()
  for(i in 1:length(my_list)){
    if(nrow(my_list[[i]]) != 0){
      #Rename data frame to match subject screening number
      names(my_list)[i] <- my_list[[i]][1,1]
    }else{
      tb_rm <- append(tb_rm, i)
    }
  } 
  #Return new data frame list without empty data sets
  return(my_list[-tb_rm])
}

#Check for 'medication taken?' errors in data sets that are ordered by date
#This function will miss errors last entries in data set and at N/Y change
df_med_check <- function(my_list){
  my_errors <- list("Query site for 'medication taken?' error:")
  #Check first entries
  for(i in 1:length(df_list)){
    if(df_list[[i]][1,3] == "Y" & length(unique(df_list[[i]][[3]])) > 1){
      my_errors <- append(my_errors,
                      paste(names(df_list)[i],"at",
                           as.character(df_list[[i]][1,2]),sep = ' '))
      df_list[[i]][1,3] <- "N"
    }else if(df_list[[i]][1,3] == "Y" & length(unique(df_list[[i]][[3]])) == 1){
      my_errors <- append(my_errors, paste(names(df_list)[i],
                                          "is missing baseline data",sep = ' '))  
    }
  }
  #Iterate through list of data frames, check for incorrect entry on other days
  for(i in 1:length(df_list)){
    for(j in 2:(nrow(df_list[[i]])-1)){
      if(df_list[[i]][j,3] == "Y" & df_list[[i]][j,3] != df_list[[i]][j-1,3] & 
        df_list[[i]][j,3] != df_list[[i]][j+1,3]){
        my_errors <- append(my_errors,
                        paste(names(df_list)[i],"at",
                           as.character(df_list[[i]][j,2]),sep = ' '))
        df_list[[i]][j,3] <- df_list[[i]][j+1,3]
      }
    }
  }
  return(list(df_list,my_errors))
}

#Function to pull individual subject data from SZL data set
df_listing <- function(i){
  #Filter seizure data frame and return seizure data for each subject
  df <- SZL %>%
         mutate(TOTSZR = rowSums(SZL[,c(17,19,21)],na.rm = T)) %>%
                                 filter(SUBNUM == subject_list[i,3]) %>% 
                                            select(SUBNUM,MEDDAT,MEDYN,TOTSZR)
  return(df)
}

#Function to partition a list of data frames into pre and post OLE
df_split_OLE <- function(df_list,df_aux,fragment){
  #Iterate through list of data frames
    for(i in 1:length(df_list)){
      #Find cutoff point
      my_cutoff <- (df_aux %>%
                           filter(SUBNUM == names(df_list)[i]) %>%
                                                             select(DSEXDT))[1,]
      #If there is no cutoff point, then there is no need to alter df lists
      if(is.na(my_cutoff)){next}
      #If fragment == 1, take the first partition
      #else take the second
      if(fragment == 1){
        #If the subject is in the EOS data set and the OLE start date is not after
        #the final day recorded, then proceed
        if(any(df_aux[[2]] == names(df_list)[i]) == T & nrow(df_list[[i]]) > 0 &
          as.integer(my_cutoff) < as.integer(df_list[[i]][nrow(df_list[[i]]),2])){
          #Set OLE start date
          temp <- as.integer(df_list[[i]][[2]])
          OLE_start_row <- min(which(temp == as.integer(my_cutoff)))
          df_list[[i]] <- df_list[[i]][1:OLE_start_row,]
        }
      }else if(fragment == 2){
        #If the subject is in the EOS data set and the OLE start date is not after
        #the final day recorded, then proceed
        if(any(df_aux[[2]] == names(df_list)[i]) == T & nrow(df_list[[i]]) > 0 &
          as.integer(my_cutoff) < as.integer(df_list[[i]][nrow(df_list[[i]]),2])){
          #Set OLE start date
          temp <- as.integer(df_list[[i]][[2]])
          OLE_start_row <- min(which(temp == as.integer(my_cutoff)))
          df_list[[i]] <- df_list[[i]][OLE_start_row:nrow(df_list[[i]]),]
        }else{
          df_list[[i]] <- NA
        }
      }
    }
  return(df_list)
}

#Function to isolate baseline and treatment phases
df_split_trt <- function(df_list,fragment){
  if(fragment == 1){#Baseline
    for(i in 1:length(df_list)){
      df_list[[i]] <- df_list[[i]][which(df_list[[i]][,3] == 'N'),]
    }
  }else if(fragment == 2){#Treatment
    for(i in 1:length(df_list)){
      df_list[[i]] <- df_list[[i]][which(df_list[[i]][,3] == 'Y'),]
    }
  }

  return(df_list)
}

#Function to remove first four lines from a data frame  
#(function also renames columns based on entries in row 4 before removing)
df_cut <- function(df){
  #Remove first four lines of data frame
  names(df) <- as.matrix(df[4,])
  df <- df[-(1:4),]
  
  return(df)
}

#Function to count the number of baseline days
df_daycount_base <- function(i){
  if(any(names(df_list) == df_sum[i,2]) == T){
    x <- which(names(df_list) == df_sum[i,2])
    return(length(which(df_list[[x]][!duplicated(df_list[[x]][,2]),][,3] == 'N')))
  }else{
    return(0)
  }
}

#Function to count the number of treatment days
df_daycount_trt <- function(i){
  #If subject has seizure data and has recorded treatment days, then count days
  if(any(names(df_list) == df_sum[i,2]) == T){
     x <- which(names(df_list) == df_sum[i,2])
     return(nrow(df_list[[x]]) - df_sum[i,4])
  }else{
     return(0)
  }
}

#Function to return the sum of seizure count column for subjects at baseline
df_colsum_base <- function(i){
  #If the subject exists in df_list
  if(any(names(df_list) == df_sum[i,2]) == T){
    #Find column, return sum. 'No': baseline. 'Yes': treatment 
    x <- which(names(df_list) == df_sum[i,2])
    datuse <- na.omit(df_list[[x]] %>% filter(df_list[[x]][,3] == 'N') %>%
                                                              select(all_of(4)))
    return(sum(datuse))
  }else{
    return(0)
  }
}

#Function to return the sum of seizure count column for subjects at baseline
df_colsum_trt <- function(i){
  #If the subject exists in df_list
  if(any(names(df_list) == df_sum[i,2]) == T){
    #Find column, return sum. 'No': baseline. 'Yes': treatment 
    x <- which(names(df_list) == df_sum[i,2])
    datuse <- na.omit(df_list[[x]] %>% filter(df_list[[x]][,3] == 'Y') %>%
                                                              select(all_of(4)))
    return(sum(datuse))
  }else{
    return(0)
  }
}

#Function to count total number of OLE seizures
df_colsum_OLE <- function(i){
  #Find column, return sum. 'No': baseline. 'Yes': treatment 
  datuse <- na.omit(df_list_OLE[[i]] %>% select(all_of(4)))
  
  return(sum(datuse))
}

#Function to build out BASELINE/TREATMENT part of 4-week view
df_4week_coladd <- function(df,df_list,study_phase){
  
  if(study_phase == 'BASELINE')
    Y.N <- 'N'
  else if(study_phase == 'TREATMENT')
    Y.N  <- 'Y'
  
  my_max <- 0
  for(i in 1:length(df_list)){
    days <- nrow(df_list[[i]] %>% filter(MEDYN == Y.N))
    if(days >  my_max){
      my_max <- days
    }
  }
  col_add <- round.off(my_max/28,digits = 0)
  #Add columns
  week_count <- 1
  for(i in 1:col_add){
    df <- add_column(df,rep(NA,nrow(df)))
    names(df)[ncol(df)] <- paste("Seizures per 28 days for",study_phase,"weeks",
                                          week_count,"-",week_count+3,sep = " ")
    week_count <- week_count+4
  }
  return(df)
}

#Function to build out OLE part of 4-week view
df_4week_coladd_OLE <- function(df,df_list){
  my_max <- 0
  for(i in 1:length(df_list)){
    if(is.na(df_list[i])){
      next
    }else if(nrow(df_list[[i]]) >  my_max){
      my_max <- nrow(df_list[[i]])
    }
  }
  col_add <- round.off(my_max/28,digits = 0)
  
  #Add columns
  week_count <- 1
  for(i in 1:col_add){
    df <- add_column(df,rep(NA,nrow(df)))
    names(df)[ncol(df)] <- paste("Seizures per 28 days for OLE weeks",
                                          week_count,"-",week_count+3,sep = " ")
    week_count <- week_count+4
  }
  return(df)
}

#Function to return percentage change between two variables
df_perc_change <- function(df){

  #Eliminate NAs from seizure rows
  df$seizures_per_day_BASE[is.na(df$seizures_per_day_BASE)] <- 0
  df$seizures_per_day_TRT[is.na(df$seizures_per_day_TRT)] <- 0
  
  #Add percentage change values to each row
  for(i in 1:nrow(df)){
    if(df[i,7] > 0){
      baseSPD <- df[i,'seizures_per_day_BASE']
      trtSPD <- df[i,'seizures_per_day_TRT']
      df[i,'percentage_change'] <- round.off((((trtSPD/baseSPD) - 1) * 100),digits = 2)
    }else{
      df[i,'percentage_change'] <- NA
    }
  }
  return(df) 
}

#Function to return comments based on percentage change
df_perc_change_comments <- function(df){
  #Go through percent change column and insert comments accordingly
  for(i in 1:nrow(df)){
    if(is.na(df[i,'percentage_change']) == T){
    next  
    }else if((df[i,'percentage_change'] <= -50) == T){
     df[i,'change_comment'] <- "More than 50% improvement" 
    }else if((df[i,'percentage_change'] %gl% c(-50,0)) == T){
      df[i,'change_comment'] <- "Improvement" 
    }else if(df[i,'percentage_change'] == 0){
      df[i,'change_comment'] <- "No change"
    }else{
      df[i,'change_comment'] <- "No improvement"
    }
  }
  
  return(df)
}

#Function to fill out the completion statuses of each subject
df_completion_status <- function(df_sum,subject_list,EOS){
  for(i in 1:nrow(df_sum)){
    #x = the completion status according to the subject list
    x <- subject_list %>%
                      filter(Subject == df_sum[i,'screening_num'])  %>%
                                                                  select(Status)
    if(x == 'Randomized'){
      df_sum[i,11] <- 'In study'
    }else if(grepl("Enrolled- OLE",x)){
      df_sum[i,11] <- 'In open label extension'
    }else if(grepl("Completed- OLE",x)){
      df_sum[i,11] <- 'Completed open label extension'
    }else{
      df_sum[i,11] <- x
    }
  }
  
  for(i in 1:nrow(df_sum)){
    #If the subject exists in the EOS data set, find the reason for study exit
    if(any(EOS[,2]  == df_sum[i,'screening_num'])){
      y <- EOS %>%
              filter(SUBNUM == df_sum[i,'screening_num'])  %>%
                                                        select(DSOPNEX,DSOTHCOM)
      #If the subject did not continue to open label extension, add reason
      if(y[1,1] == 'N'){
        df_sum[i,11] <- y[1,2]
      }
    }
  }
  return(df_sum)
}

#Function to fill out the 4 week analysis data set
df_4week <- function(df_monthly,df_list){
  #Iterate through data frame list and input monthly seizure count
  month_count <- 1
  j = 2
  while(j <= ncol(df_monthly)){
    for(i in 1:nrow(df_monthly)){
      if(any(names(df_list) == df_monthly[i,1]) == T){
        df <- df_list[[which(names(df_list) == df_monthly[i,1])]]
        if(nrow(df) >= month_count+27){
          df_monthly[i,j] <- sum(df[month_count:(month_count+27),4])
        }
        else if(nrow(df) < (month_count+27) & nrow(df) >= month_count){
          df_monthly[i,j] <- round.off((sum(df[month_count:nrow(df),4])/(nrow(df)-
                                                  (month_count-1)))*28, digits = 2)
        }
      }
    }
    month_count <- month_count+28
    j <- j + 1
  }
  return(df_monthly)
}

#Function to fill out the OLE entries in the 4 week analysis data set
df_4week_OLE <- function(df_monthly,df_list){
  #Iterate through data frame list and input monthly seizure count
  month_count <- 1
  j = 2
  while(j <= ncol(df_monthly)){
    for(i in 1:nrow(df_monthly)){
      if(any(OLE_keep == df_monthly[i,1]) == F){next}
      if(is.na(df_list[which(names(df_list) == df_monthly[i,1])]) == F){
        df <- df_list[[which(names(df_list) == df_monthly[i,1])]]
        if(nrow(df) >= month_count+27){
          df_monthly[i,j] <- round.off(sum(df[month_count:(month_count+27),4]),digits = 2)
        }
        else if(nrow(df) < (month_count+27) & nrow(df) >= month_count){
          df_monthly[i,j] <- round.off((sum(df[month_count:nrow(df),4])/(nrow(df) -
                                                  (month_count-1)))*28,digits = 2)
        }
      }
    }
    month_count <- month_count+28
    j <- j + 1
  }
  return(df_monthly)
}

#Function for plotting seizures per day for each subject after drug is taken
df_plots <- function(my_list){
  #Iterate through the list of data frames and find the total number of rows
  total_rows <- 0
  for(i in 1:length(my_list)){
    if(nrow(my_list[[i]])>0){
    total_rows = total_rows+nrow(my_list[[i]])
    }
  }
  #Eliminate NA's
  for(i in 1:length(my_list)){
    my_list[[i]][,4][is.na(my_list[[i]][,4])] = 0
  }
  #Make data frame to be used for plots
  df_fin <- data.frame(matrix(ncol = 4, nrow = total_rows))
  #Edit column names
  names(df_fin) <- c("day_count", "subject", "drug_taken", "s_count")
  #Fill data frame up to moving average
  start_pt <- 1
  end_pt <- 0
  for(i in 1:length(my_list)){
    if(nrow(my_list[[i]])>0){
      end_pt = end_pt+nrow(my_list[[i]])
      day_count = 1
        for(j in start_pt:end_pt){
        df_fin[j,"day_count"] <- day_count
        df_fin[j, "subject"] <- names(my_list[i])
        df_fin[j, "drug_taken"] <- my_list[[i]][day_count,3]
        df_fin[j, "s_count"] <- my_list[[i]][day_count,4]
        day_count = day_count + 1
      }
      start_pt = start_pt+nrow(my_list[[i]])
    }
  }
  #Make data frame for plots
  datuse <- df_fin %>% filter(drug_taken == "Y") %>%
                                      select(day_count, subject, s_count)
  #Add moving average column
  datuse$moving_average <- NA
  #Fill moving average column
  for(i in 1:nrow(datuse)){
    datuse[i,'moving_average'] <- mean(datuse[min(which(datuse$subject == 
                                            datuse[i,'subject'])):i,'s_count'])
  }
  #Create plots for data
  #Regular tracking line
  plot_s_count <- ggplot(data = datuse, aes(x = day_count, y = s_count)) +
    geom_line(aes(color = subject), size = 1) +
    ggtitle("Count of daily seizures over time (medication taken) \nStudy: EQU-201") +
    xlab("Days") +
    ylab("Seizure Count")
  #Moving average line
  plot_moving_av <- ggplot(data = datuse, aes(x = day_count, y = moving_average)) +
    geom_line(aes(color = subject), size = 1) +
    scale_y_continuous(limit=c(0,NA), oob=squish) +
    ggtitle("Moving average of daily seizures over time (medication taken) \nStudy: EQU-201") +
    xlab("Days") +
    ylab("Moving Average")
  #Print plots
  print(plot_s_count) 
  print(plot_moving_av)
}

#Function for plotting seizures per day for each subject after drug is taken (OLE)
df_plots_OLE <- function(my_list){
  #Iterate through the list of data frames and find the total number of rows
  total_rows <- 0
  for(i in 1:length(my_list)){
    if(typeof(my_list[[i]]) != 'logical'){
      if(nrow(my_list[[i]])>0){
        total_rows = total_rows+nrow(my_list[[i]])
      }
    }
  }
  #Eliminate NA's
  for(i in 1:length(my_list)){
    if(typeof(my_list[[i]]) != 'logical'){
     my_list[[i]][,4][is.na(my_list[[i]][,4])] = 0
    }
  }
  #Make data frame to be returned
  df_fin <- data.frame(matrix(ncol = 3, nrow = total_rows))
  #Edit column names
  names(df_fin) <- c("day_count", "subject", "s_count")
  #Fill data frame up to moving average
  start_pt <- 1
  end_pt <- 0
  for(i in 1:length(my_list)){
    if(typeof(my_list[[i]]) != 'logical'){
      if(nrow(my_list[[i]])>0){
        end_pt = end_pt+nrow(my_list[[i]])
        day_count = 1
        for(j in start_pt:end_pt){
          df_fin[j,"day_count"] <- day_count
          df_fin[j, "subject"] <- df_names[[i]]
          df_fin[j, "s_count"] <- my_list[[i]][day_count,4]
          day_count = day_count + 1
        }
        start_pt = start_pt+nrow(my_list[[i]])
      }
    }
  }
  #Make data frame for plots
  datuse <- df_fin
  #Add moving average column
  datuse$moving_average <- NA
  #Fill moving average column
  for(i in 1:nrow(datuse)){
    datuse[i,'moving_average'] <- mean(datuse[min(which(datuse$subject == 
                                             datuse[i,'subject'])):i,'s_count'])
  }
  #Create plots for data
  #Regular tracking line
  plot_s_count <- ggplot(data = datuse, aes(x = day_count, y = s_count)) +
    geom_line(aes(color = subject), size = 1) +
    ggtitle("Count of daily seizures over time (open label extension) \nStudy: EQU-201") +
    xlab("Days") +
    ylab("Seizure Count")
  #Moving average line
  plot_moving_av <- ggplot(data = datuse, aes(x = day_count, y = moving_average)) +
    geom_line(aes(color = subject), size = 1) +
    scale_y_continuous(limit=c(0,NA), oob=squish) +
    ggtitle("Moving average of daily seizures over time (open label extension) \nStudy: EQU-201") +
    xlab("Days") +
    ylab("Moving Average")
  #Print plots
  print(plot_s_count) 
  print(plot_moving_av)
}




