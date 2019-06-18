
# Construct data
X = matrix(rnorm(100),10,10); for (i in 2:10) X[,i]=X[,i]+X[,i-1] + i*rnorm(10)
covmat = cov(X)

# Construct eigenvalues and vectors
e = eigen(covmat)
evalues = e$values
stdevPC = sqrt(evalues)
plot(sort(evalues, decreasing = T))
lines(sort(evalues, decreasing = T), col = 'blue')

loadings <- e$vectors %*% sqrt(diag(e$values, nrow = length(e$values)))
communalities <- rowSums(loadings^2)
communalities <- loadings^2
sign.tot <- sign(colSums(loadings))
sign.tot[sign.tot == 0] <- 1
loadings <- loadings %*% diag(sign.tot)

