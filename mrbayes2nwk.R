library(ape)
files <- list.files(path="/home/tarakark/AutoCogPhylo/glottcode_nexus_out", pattern="*.run1.t$", full.names=T, recursive=FALSE)
lapply(files, function(x) {

fname <- paste(x,".nwk",sep="")

# 
if(!file.exists(fname) & grepl("-ie-", fname)){
print(x)
t <- read.nexus(x)
if(grepl("svm", fname)){
t<- lapply(t, drop.tip,tip=c("irrr1240"))
class(t)<-"multiPhylo"
#t <- drop.tip(t,"irrr1240")
}
write.tree(t, file=fname)
}
}
)
