#######################################################
#######################################################
###########Principal Component Analysis################
#######################################################
#######################################################



#######################
#####Tools for PCA#####
#######################
library(psych) #Library that contains helpful PCA functions, such as:

principal() #Performs principal components analysis with optional rotation.
fa.parallel() #Creates scree plots with parallell analyses for choosing K.
factor.plot() #Visualizes the principal component loadings.


############################
#####Data for Example 1#####
############################
bodies = Harman23.cor$cov #Covariance matrix of 8 physical measurements on 305 girls.
bodies



####################
#####Choosing K#####
####################
fa.parallel(bodies, #The data in question.
            n.obs = 305, #Since we supplied a covaraince matrix, need to know n.
            fa = "pc", #Display the eigenvalues for PCA.
            n.iter = 100) #Number of simulated analyses to perform.
abline(h = 1) #Adding a horizontal line at 1.

#1. Kaiser-Harris criterion suggests retaining PCs with eigenvalues > 1; PCs with
#   eigenvalues < 1 explain less varaince than contained in a single variable.
#2. Cattell Scree test visually inspects the elbow graph for diminishing return;
#   retain PCs before a drastic drop-off.
#3. Run simulations and extract eigenvalues from random data matrices of the same
#   dimension as your data; find where the parallel analysis overshadows real data.



########################
#####Performing PCA#####
########################
pc_bodies = principal(bodies, #The data in question.
                      nfactors = 2, #The number of PCs to extract.
                      rotate = "none")
pc_bodies

#-PC columns contain loadings; correlations of the observed variables with the PCs.
#-h2 column displays the component comunalities; amount of variance explained by
# the components.
#-u2 column is the uniqueness (1 - h2); amount of varaince NOT explained by the
# components.
#-SS loadings row shows the eigenvalues of the PCs; the standardized varaince.
#-Proportion/Cumulative Var row shows the variance explained by each PC.
#-Proportion Explained/Cumulative Proportion row considers only the selected PCs.



########################################
#####Visualizing & Interpreting PCA#####
########################################
factor.plot(pc_bodies,
            labels = colnames(bodies)) #Add variable names to the plot.

#-PC1 correlates highly positively with length-related variables (height, arm
# span, forearm, and lower leg). This is a "length" dimension.
#-PC2 correlates highly positively with volume-related variables (weight, bitro
# diameter, chest girth, and chest width). This is a "volume" dimension.



############################
#####Data for Example 2#####
############################
iris_meas = iris[, -5] #Measurements of iris dataset.
iris_meas
plot(iris_meas)



####################
#####Choosing K#####
####################
fa.parallel(iris_meas, #The data in question.
            fa = "pc", #Display the eigenvalues for PCA.
            n.iter = 100) #Number of simulated analyses to perform.
abline(h = 1) #Adding a horizontal line at 1.
#Should extract 1 PC, but let's look at 2.



########################
#####Performing PCA#####
########################
pc_iris = principal(iris_meas, #The data in question.
                    nfactors = 2,
                    rotate = "none") #The number of PCs to extract.
pc_iris

factor.plot(pc_iris,
            labels = colnames(iris_meas)) #Add variable names to the plot.

#-PC1 separates out the importance of the sepal width as cotrasted with the
# remaining variables.
#-PC2 contrasts the differences between the sepal and petal measurements.



################################
#####Viewing Projected Data#####
################################
plot(iris_meas) #Original data: 4 dimensions.
plot(pc_iris$scores) #Projected data: 2 dimensions.



############################
#####Data for Example 3#####
############################
library(Sleuth2)
case1701
printer_data = case1701[, 1:11]

fa.parallel(printer_data, #The data in question.
            fa = "pc", #Display the eigenvalues for PCA.
            n.iter = 100) #Number of simulated analyses to perform.
abline(h = 1) #Adding a horizontal line at 1.
#Should extract 1 PC, but let's look at 3.

pc_printer = principal(printer_data, #The data in question.
                       nfactors = 3,
                       rotate = "none") #The number of PCs to extract.
pc_printer

factor.plot(pc_printer) #Add variable names to the plot.

#-PC1 ends up being a weighted average.
#-PC2 contrasts one side of the rod with the other.
#-PC3 contrasts the middle of the rod with the sides of the rod.

plot(printer_data)
pairs(pc_printer$scores)



### Preprocess with PCA with caret
library(caret)

### The number of principal components kept can be decided by
### 1. thres: set the threshold for cumulative variance
### 2. pcaComp: set explicitlythe amount to be kept
### If pcaComp is set, thres would be ignored

ctrl <- trainControl(preProcOptions = list(thres = 0.90,
                                           pcaComp = 3))

md = train(Species ~ ., data = iris,
           method = 'glmnet',
           preProc = 'pca',
           family = 'multinomial',
           trControl = ctrl)

### The predictors included in the final model
md$finalModel$xNames
