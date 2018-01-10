library(ggplot2)
library(cowplot)
library(HDInterval)

theme_set(theme_grey())
data_summary <- function(x) {
    bayes <- hdi(x, credMass=0.95)
    m <- median(x)
    ymin <- unname(bayes[1])
    ymax <- unname(bayes[2])
    return(c(y=m,ymin=ymin,ymax=ymax))
 }

st <- read.table("sinotebetean_gqd.csv" ,header=TRUE, sep=",")
abvd <- read.table("ABVD.csv" ,header=TRUE, sep=",")
IE <- read.table("IELEX_GQD.tsv" ,header=TRUE, sep=",")
tng <- read.table("Trans_New.csv" ,header=TRUE, sep=",")
st$Method <- as.factor(st$Method)
abvd$Method <- as.factor(abvd$Method)
IE$Method <- as.factor(IE$Method)
tng$Method <- as.factor(tng$Method)



pt <- "Set1"


p_ie <- ggplot(IE, aes(x=Method, y=GQD, color=Method, fill=Method))+geom_violin(trim=TRUE)+
        stat_summary(fun.data=data_summary, color="black")+ggtitle("Indo-European")+
        scale_x_discrete(limits=c("manual", "lexstat", "svm"))+scale_fill_brewer(palette=pt)+
        scale_color_brewer(palette=pt)+theme(legend.position = "none", axis.title.x=element_blank(),
        axis.text.x=element_blank(),axis.ticks.x=element_blank(),plot.title=element_text(hjust=0.5))

p_abvd <- ggplot(abvd, aes(x=Method, y=GQD, color=Method, fill=Method))+geom_violin(trim=FALSE)+
        stat_summary(fun.data=data_summary, color="black")+ggtitle("Austronesian")+
        scale_x_discrete(limits=c("manual", "lexstat", "svm"))+scale_fill_brewer(palette=pt)+
        scale_color_brewer(palette=pt)+theme(legend.position = "none", axis.title.x=element_blank(),
        axis.text.x=element_blank(),axis.ticks.x=element_blank(),axis.title.y=element_blank(),plot.title=element_text(hjust=0.5))

p_tng <- ggplot(tng, aes(x=Method, y=GQD, color=Method, fill=Method))+geom_violin(trim=FALSE)+
        stat_summary(fun.data=data_summary, color="black")+ggtitle("Trans-New Guinea")+
        scale_x_discrete(limits=c("manual", "lexstat", "svm"))+scale_fill_brewer(palette=pt)+
        scale_color_brewer(palette=pt)+theme(legend.position = "none",axis.title.y=element_blank(),plot.title=element_text(hjust=0.5))

p_st <- ggplot(st, aes(x=Method, y=GQD, color=Method, fill=Method))+geom_violin(trim=FALSE)+
        stat_summary(fun.data=data_summary, color="black")+ggtitle("Sino-Tibetean")+
        scale_x_discrete(limits=c("manual", "lexstat", "svm"))+scale_fill_brewer(palette=pt)+
        scale_color_brewer(palette=pt)

legend <- get_legend(p_st)
p_st <- p_st + theme(legend.position = "none",plot.title=element_text(hjust=0.5))

plots <- align_plots(p_ie, p_abvd, p_st, align = 'v', axis = 'l')
bottom_row <- plot_grid(plots[[3]], legend, nrow = 1)
top_row <- plot_grid(plots[[1]], plots[[2]], nrow = 1)


pdf("violin_all_bayes.pdf")
plot_grid(top_row,bottom_row, ncol = 1)
dev.off()



IE.man <- IE[ which(IE$Method == "manual"),]
IE.svm <- IE[ which(IE$Method == "svm"),]
IE.lex <- IE[ which(IE$Method == "lexstat"),]

ST.man <- st[ which(st$Method == "manual"),]
ST.svm <- st[ which(st$Method == "svm"),]
ST.lex <- st[ which(st$Method == "lexstat"),]

ABVD.man <- abvd[ which(abvd$Method == "manual"),]
ABVD.svm <- abvd[ which(abvd$Method == "svm"),]
ABVD.lex <- abvd[ which(abvd$Method == "lexstat"),]

hdi(IE.svm$GQD, credMass=0.95)
median(IE.svm$GQD)

hdi(IE.lex$GQD, credMass=0.95)
median(IE.lex$GQD)

hdi(IE.man$GQD, credMass=0.95)
median(IE.man$GQD)


hdi(ST.svm$GQD, credMass=0.95)
median(ST.svm$GQD)

hdi(ST.lex$GQD, credMass=0.95)
median(ST.lex$GQD)

hdi(ST.man$GQD, credMass=0.95)
median(ST.man$GQD)


hdi(ABVD.svm$GQD, credMass=0.95)
median(ABVD.svm$GQD)

hdi(ABVD.lex$GQD, credMass=0.95)
median(ST.lex$GQD)

hdi(ABVD.man$GQD, credMass=0.95)
median(ABVD.man$GQD)
