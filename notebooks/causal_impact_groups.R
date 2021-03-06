library(CausalImpact)
library(feather)
library(ggplot2)
library(rjson)

parameters = fromJSON(file="../data/causal_impact/parameters.json")
alpha = parameters$alpha
input_path = parameters$input_path
output_path = parameters$output_path
  

df = read_feather(input_path) 
groups = unique(df$group)

results_list <- list()
count = 1

for (group in groups){
    print(group)
    df_group = df[df$group==group, ]
    
    min_date = min(df_group$fecha)
    max_date = max(df_group$fecha)
    pre_max = max(df_group[df_group$pre_period_flag==1,]$fecha)
    post_min = min(df_group[df_group$pre_period_flag==0,]$fecha)
    pre.period <- as.POSIXct(c(min_date, pre_max))
    post.period <- as.POSIXct(c(post_min, max_date))
    
    x = df_group[ , grepl("x", names(df_group))]
    data = cbind(y=df_group$y, x)
    data <- zoo(data, df_group$fecha)
    
    impact <- CausalImpact(data, pre.period, post.period, alpha=alpha)#, model.args = list(nseason=52))
    impact.plot <- plot(impact)
    impact.plot <- impact.plot + theme_bw(base_size = 10) +
                 ggtitle(paste("Impact of covid for ", group, sep=" "))
    print(impact.plot)
    results = data.frame(impact[[1]])
    results$group = group
    results$fecha = df_group$fecha
    results_list[[count]] <- results
  
    
    count <- count + 1
}
all_results = do.call(rbind, results_list) #concatenate list of dataframes
write_feather(all_results, output_path)