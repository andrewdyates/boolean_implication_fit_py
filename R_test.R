M <- as.matrix(read.table("nice.may3.Eg.expr.gold.celegans.csv", sep=",", header=TRUE, row.names=1))
source("../boolean_implication_fit/step.up.R")
source("../boolean_implication_fit/bool.R")

all.steps <- function(M, do.plot=TRUE) {
  STEPS <- apply(M, 1, fit.upstep)
  if(do.plot) {
    for (i in 1:dim(M)[1]) {
      title=rownames(M)[i]
      plot.stepfit(STEPS[[i]], v=M[i,], add.mean.median=T, main=paste(title, "Stepfit"))
      plot.sse(STEPS[[i]], add.mean.median=T, main=paste(title, "SSE"))
    }
  }
  STEPS
}

all.pairs.cls <- function(M, steps, b=0.5, do.plot=TRUE) {
  n <- dim(M)[1]
  CLS <- mat.or.vec(n,n)
  for(i in 1:n) { # row
    for(j in 1:n) { # col
      y <- M[i,]
      y.th <- steps[[i]]$th
      x <- M[j,]
      x.th <- steps[[j]]$th
      x.title=rownames(M)[j]
      y.title=rownames(M)[i]
      RR <- cls.pair(x,y,x.th,y.th, b.x=b, b.y=b, do.plot=(i<j)&&do.plot, xlab=x.title, ylab=y.title)
      CLS[i,j] <- cls.to.enum(RR$CLS)
    }
  }
  rownames(CLS) <- rownames(M)
  colnames(CLS) <- rownames(M)
  CLS
}

b <- 0.3
STEPS <- all.steps(M, do.plot=F)
pdf("bool.plots.pdf")
CLS <- all.pairs.cls(M, STEPS, b, do.plot=T)
dev.off()
write.table(CLS, file="R_cls.tab", sep="\t", quote=F)


i <- 5
j <- 7
y <- M[i,]
y.th <- STEPS[[i]]$th
x <- M[j,]
x.th <- STEPS[[j]]$th
x.title=rownames(M)[j]
y.title=rownames(M)[i]
pdf("hnd1.cwn1.bool.pdf")
R <- cls.pair(x,y,x.th,y.th, b.x=b, b.y=b, do.plot=T, xlab=x.title, ylab=y.title)
dev.off()
