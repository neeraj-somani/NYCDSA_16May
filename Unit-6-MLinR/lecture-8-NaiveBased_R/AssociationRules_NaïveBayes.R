###########################################################
###########################################################
#####[13] Association Rules & Naïve Bayes Lecture Code#####
###########################################################
###########################################################



#####################################
#####Tools for Association Rules#####
#####################################
#Attempting to read the groceries data in the original way.
not.useful = read.csv("Groceries.csv", header = FALSE)
head(not.useful)
View(not.useful)

#Two different problems arise:
#- Splitting our data into chunks of 4 because of the first row of our dataset;
#  what about when we have transactions with more than 4 items?
#- Creating features that not only include the items that were purchased,
#  but also the artificial order in which they were purchased. Technically,
#  there is no order to a basket of items, just whether or not the items were
#  included in the transaction.

#Instead, let's create a sparse matrix. The different items will represent the
#columns and the rows will represent the transactions; essentially we are
#creating an indicator variable for each available item. The resulting matrices
#will be quite large; under the hood, the sparse matrix that we are creating
#using the read.transactions() function is only actually storing the 1's among
#the millions of cells.

#Load the Association Rules library and store the groceries data in a sparse
#matrix.
library(arules)
groceries = read.transactions("Groceries.csv", sep = ",")

#Inspecting the groceries object we just created.
groceries
class(groceries)
dim(groceries)
colnames(groceries)
rownames(groceries)

#Gathering summary information for the groceries object we just created.
summary(groceries)

#Inspecting the distribution of transaction size.
size(groceries)
hist(size(groceries))

#Using the inspect() function to look at the actual contents of the sparse
#matrix. In particular, looking at each tranasction.
inspect(groceries[1:10])

#Using the itemFrequency() function to look at the actual contents of the sparse
#matrix. In particular, looking at each item.
itemFrequency(groceries[, 1:5], type = "relative") #Default
itemFrequency(groceries[, 1:5], type = "absolute")

#Using the itemFrequencyPlot() function to visualize item frequencies.
itemFrequencyPlot(groceries)
itemFrequencyPlot(groceries, support = 0.1)
itemFrequencyPlot(groceries, topN = 20)

#Visualizing the binary relationship among transactions and items.
set.seed(0)
image(sample(groceries, 100))

#Using the apriori() function to look for association rules using the Apriori
#algorithm.
apriori(groceries,
        parameter = list(support = .1,     #Default minimum support.
                         confidence = .8,  #Default minimum confidence.
                         minlen = 1,       #Default minimum set size.
                         maxlen = 10))     #Default maximum set size.

#Creating some rules by lowering the support and confidence.
groceryrules = apriori(groceries,
                       parameter = list(support = 0.006,
                                        confidence = 0.25,
                                        minlen = 2))

#Investigating summary information about the rule object.
groceryrules
class(groceryrules)
summary(groceryrules)

#Inspecting specific information about rules.
inspect(groceryrules[1:5])

#Sorting the rules by various metrics.
inspect(sort(groceryrules, by = "support")[1:5])
inspect(sort(groceryrules, by = "confidence")[1:5])
inspect(sort(groceryrules, by = "lift")[1:5])

#Finding subsets of rules based on a particular item.
berryrules = subset(groceryrules, items %in% "berries")
inspect(berryrules)

herbrules = subset(groceryrules, items %in% "herbs")
inspect(herbrules)



###############################
#####Tools for Naïve Bayes#####
###############################
#Reading in the raw SMS data into a data frame; ensuring that the strings
#aren't converted to factors.
sms_raw = read.csv("SMSSpam.csv", stringsAsFactors = FALSE)

#Examining the structure of the sms data; two columns, one of the actual text itself
#and one displaying whether or not the observation is spam.
str(sms_raw)
View(sms_raw)

#Overwriting the type variable to convert it to a factor.
sms_raw$type = as.factor(sms_raw$type)

#Inspecting the new type variable.
str(sms_raw$type)
table(sms_raw$type)

#Installing the Text Mining package for the purpose of processing text data
#for analysis; installing the SnoballC library for stemming purposes.
library(tm)
library(SnowballC)

#Creating a corpus with the text message data; VectorSource() interprets each
#element of the vector that it is passed as an individual document.
sms_corpus = Corpus(VectorSource(sms_raw$text))

#Examining the overall contents of the SMS corpus.
sms_corpus

#Examining the specific contents of the SMS corpus; converting the plain text
#documents to character strings.
tm::inspect(sms_corpus[1:3])
lapply(sms_corpus[1:3], as.character)

#Loading the wordcloud library to help visualize our corpus data.
library(wordcloud)
wordcloud(sms_corpus, min.freq = 50) #Freq. of about 1% of the documents.
wordcloud(sms_corpus, min.freq = 50, random.order = FALSE) #Order by frequency.

#Subsetting the data into spam and ham groups.
spam = subset(sms_raw, type == "spam")
ham = subset(sms_raw, type == "ham")

#The wordcloud() function is versatile enough to automatically apply some text
#transformation and tokenization processes to raw data; we will transform our
#raw data for modeling purposes in a moment.
wordcloud(spam$text, max.words = 40)
wordcloud(ham$text, max.words = 40)

#Cleaning up the SMS corpus by performing transformations of the text data; converting
#all characters to lowercase, removing numbers, removing stopwords, removing punctuation,
#and stemming words. Creating a sparse document term matrix; this is called tokenization.
sms_dtm = DocumentTermMatrix(sms_corpus, control = list(
  tolower = TRUE,
  removeNumbers = TRUE,
  stopwords = function(x) { removeWords(x, stopwords()) },
  removePunctuation = TRUE,
  stemming = TRUE
))

#Creating training and test sets with a 75% - 25% split; the observations are
#listed in random order.
sms_dtm_train = sms_dtm[1:4169, ]
sms_train_labels = sms_raw[1:4169, ]$type
sms_dtm_test = sms_dtm[4170:5559, ]
sms_test_labels  = sms_raw[4170:5559, ]$type

#Checking that the proportion of spam and non-spam messages is similar among
#the training and test sets.
prop.table(table(sms_train_labels))
prop.table(table(sms_test_labels))

#Removing terms that are extremely sparse; terms that do not appear in 99.9% of
#the data.
sms_dtm_freq_train = removeSparseTerms(sms_dtm_train, sparse = 0.999)
sms_dtm_train #Before
sms_dtm_freq_train #After

#Displaying indicator features for frequent words (those that appear in at
#least approximately 0.1% of the text messages); saving the terms as a character
#vector.
findFreqTerms(sms_dtm_train, 5)
sms_freq_words = findFreqTerms(sms_dtm_train, 5)
str(sms_freq_words)

#Create sparse document term matrices with only the frequent terms.
sms_dtm_freq_train = sms_dtm_train[, sms_freq_words]
sms_dtm_freq_test = sms_dtm_test[, sms_freq_words]

#Since the Naïve Bayes classifier is typically trained on data with categorical
#features, we need to change each of the counts to indicators.
convert_counts = function(x) {
  x = ifelse(x > 0, "Yes", "No")
}

#Using the apply() function to convert the counts to indicators in the columns
#of both the training and the test data.
sms_train = apply(sms_dtm_freq_train, 2, convert_counts)
sms_test = apply(sms_dtm_freq_test, 2, convert_counts)

#Inspecting the final matrices.
head(sms_train)
summary(sms_train)

#Loading the e1071 library in order to implement the Naïve Bayes classifier.
library(e1071)

#Applying the naiveBayes() classifier function to the training data.
sms_classifier = naiveBayes(sms_train, sms_train_labels)
sms_classifier

#Evaluating the model performance by predicting the test observations.
sms_test_pred = predict(sms_classifier, sms_test)
sms_test_pred

#Creating a confusion matrix of the actual and predicted labels.
table(sms_test_pred, sms_test_labels)
(1201 + 153)/1390

#Directly out-of-the-box, the Naïve Bayes classifier performs extremely well,
#even when the assumptions are quite unrealistic. We only have an error rate
#of about 2.6%!

#Applying the Laplace estimator and inspecting the accuracy.
sms_classifier2 = naiveBayes(sms_train, sms_train_labels, laplace = 1)
sms_test_pred2 = predict(sms_classifier2, sms_test)
table(sms_test_pred2, sms_test_labels)
(1202 + 155)/1390

#Using the Laplace estimator, the error rate decreases slightly to about 2.4%;
#there was a slight reduction in both types of errors.