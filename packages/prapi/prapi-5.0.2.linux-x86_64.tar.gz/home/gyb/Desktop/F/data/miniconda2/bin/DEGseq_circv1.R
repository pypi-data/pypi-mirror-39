#!/usr/bin/env Rscript
args <- commandArgs(TRUE)
library(DEGseq)
#geneExpFile<-read.table(file=mock_ga.txt,header=T,sep="\t",row.names=1)
#outputDir <-  "args[2]"
#DEGexp2(geneExpFile1 = geneExpFile, expCol1 =(5), groupLabel1 = "mutation",geneExpFile2 = geneExpFile, expCol2 = c(2), groupLabel2 ="Wild",outputDir =outputDir, method = "MARS",pValue=1e-2,thresholdKind=1)
DEGexp2(geneExpFile1 = args[1], expCol1 =c(2), groupLabel1 = "control", geneExpFile2 = args[1],expCol2 = c(3), groupLabel2 ="mutation",outputDir = args[2], method = "MARS",pValue=1e-2,thresholdKind=0.1)
