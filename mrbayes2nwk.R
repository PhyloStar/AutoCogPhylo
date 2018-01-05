library(ape)
files <- list.files(path="/home/tarakark/AutoCogPhylo/glottcode_nexus_out", pattern="*.run1.t$", full.names=T, recursive=FALSE)
lapply(files, function(x) {
print(x)
fname <- paste(x,".nwk",sep="")

if(!file.exists(fname) & !grepl("-pn-", fname)){

t <- read.nexus(x)
if(grepl("-st-", fname){
t <- drop.tip(t,"irrr1420")
}
write.tree(t, file=fname)}
}
)
