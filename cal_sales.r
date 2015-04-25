data<-read.csv("./preprocess.csv", header=T, sep=",", colClasses = c(pid = "character"))
data.a <- aggregate( sum ~ pid, data=data, FUN=sum)
data.b <- data.a[with(data.a, order(-data.a$sum)), ]$pid[1:20]
output <- lapply(seq(20),function(i) paste(c(formatC(i, digits=2, width=2,format="d", flag="0"), data.b[i]), collapse = ","))
write(unlist(output), "r.result", sep=",")
