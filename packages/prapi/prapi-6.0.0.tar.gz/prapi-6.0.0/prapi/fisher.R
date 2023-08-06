#!/usr/bin/env Rscript
args <- commandArgs(TRUE)
a<-as.matrix(read.table(args[1], header=T))
fisher.test(a)$p.value
