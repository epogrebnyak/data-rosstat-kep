require(ggplot2)
df <- data.frame(1:10, 1:10)
colnames(df) <- c("index", "rate")
ggsample <- ggplot(df, aes(x=index, y=rate)) + geom_line()
windows(8,6)
ggsample 