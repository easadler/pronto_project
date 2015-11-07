df = read.csv("regression.csv")
names <- c('hour','dayofweek','month','season','year','terminal', 'hood','timeperiod','smallgroups')
df[names] <- lapply(df[names], as.factor)
df$count <- as.integer(df$count)
#df$count <- log(df$count)

df$Max_Gust_Speed_MPH <- as.integer(df$Max_Gust_Speed_MPH)

df_f <- df[, !(colnames(df) %in% c('Max_Wind_Speed_MPH','Mean_Visibility_Miles','Min_Humidity','Mean_Temperature_F','Max_Temperature_F','Mean_Visibility_Mile','Min_Visibility_Miles','elevation','dockcount','timeperiod','season','Max_Visibility_Miles','hood','big_cluster','smallgroups'))]

fit <- lm(count~hour + terminal + hour*terminal, data=df_f)
summary(fit)

y <- predict(fit)
y[y < 0] <- 0

plot(y,residuals(fit)) 
abline(0, 0)             
qqnorm(y) # A quantile normal plot - good for checking normality
qqline(y)
plot(df$bikeid, df$temp)
