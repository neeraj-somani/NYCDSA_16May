
# https://cran.r-project.org/web/packages/tm/vignettes/tm.pdf
# tm 
# What tm does:
# data import
# corpus handling
# preprocessing
# term-document matrix creation

# Create a corpus
# VCorpus(x, readerControl)
# x from tm::getSources()
# readerControl from tm::getReaders()

library(tm)

# Example:
txt <- system.file("texts", "txt", package = "tm")
(ovid <- Corpus(DirSource(txt, encoding = "UTF-8"),
                 readerControl = list(language = "lat")))

tm::inspect(ovid[1:2])
NLP::meta(ovid[[1]])
NLP::meta(ovid[[2]])
sapply(ovid[1:2],as.character)

# Generated Example:
doc1 = "This is my document!  Many are like it but this one is mine!  Without me ..."
doc2 = "This is another document of mine!  Many are like it but this one is mine!"
doc3 = "Yes, believe it or not, I have a third document!!!  I am very proud."
doc4 = "The word cookie will only appear once."
doc5 = "                the final frontier. These ..."

docs = c(doc1,doc2,doc3,doc4,doc5)
docs
mycorpus = VCorpus(VectorSource(docs))
mycorpus
tm::inspect(mycorpus)
sapply(mycorpus,as.character)

# Available transformation functions
tm::getTransformations()

# Required package
library(SnowballC)

# Transform the corpus:
newcorpus = tm_map(mycorpus, stripWhitespace)
sapply(newcorpus,as.character)

newcorpus = tm_map(newcorpus, removeWords, stopwords("english"))
sapply(newcorpus,as.character)

newcorpus = tm_map(newcorpus, stemDocument)
sapply(newcorpus,as.character)

newcorpus = tm_map(newcorpus, removePunctuation)
sapply(newcorpus,as.character)

# Document Term Matrix
dtm <- DocumentTermMatrix(newcorpus)
tm::inspect(dtm)
findFreqTerms(dtm,1)
findFreqTerms(dtm,2)
findFreqTerms(dtm,3)

findAssocs(x=dtm,terms ="mine", corlimit = 0.8)

# Manual Calculations
dmat = as.matrix(dtm)

# Manual Association Calculation
cor(dmat)

# Manual Sparcity Calculation
sum(dmat==0)/prod(dim(dmat))
