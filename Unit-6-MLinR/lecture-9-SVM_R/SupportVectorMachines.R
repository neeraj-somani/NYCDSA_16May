###################################################
###################################################
#####[10] Support Vector Machines Lecture Code#####
###################################################
###################################################



###################################
#####Maximal Margin Classifier#####
###################################
#Generating linearly separable data.
set.seed(0)
x1 = c(rnorm(100, 0, 4), rnorm(100, 1, 3))
x2 = c(rnorm(100, 0, 1), rnorm(100, 6, 1))
y = as.factor(c(rep(-1, 100), rep(1, 100)))
linearly.separable = data.frame(x1, x2, y)

#Plotting the linearly separable data.
plot(linearly.separable$x1, linearly.separable$x2, col = linearly.separable$y)

#Creating training and test sets.
set.seed(0)
train.index = sample(1:200, 200*.8)
test.index = -train.index

#Importing the e1071 library in order to use the svm() function to fit support
#vector machines.
library(e1071)

#Fitting a maximal margin classifier to the training data.
svm.mmc.linear = svm(y ~ ., #Familiar model fitting notation.
                     data = linearly.separable, #Using the linearly separable data.
                     subset = train.index, #Using the training data.
                     kernel = "linear", #Using a linear kernel.
                     cost = 1e6) #A very large cost; default is 1.

#Visualizing the results of the maximal margin classifier.
plot(svm.mmc.linear, linearly.separable[train.index, ])

#Additional information for the fit.
summary(svm.mmc.linear)

#Finding the indices of the support vectors.
svm.mmc.linear$index

#Predicting on the test data.
ypred = predict(svm.mmc.linear, linearly.separable[test.index, ])
table("Predicted Values" = ypred, "True Values" = linearly.separable[test.index, "y"])

#Adding a single point to display the sensitivity of the maximal margin classifier.
linearly.separable2 = rbind(linearly.separable, c(-5, 3, 1))
plot(linearly.separable2$x1, linearly.separable2$x2, col = linearly.separable2$y)

#Fitting a maximal margin classifier to the new data.
svm.mmc.linear2 = svm(y ~ .,
                      data = linearly.separable2,
                      kernel = "linear",
                      cost = 1e6)

#Visualizing the results of the maximal margin classifier; comparing the output.
plot(svm.mmc.linear, linearly.separable[train.index, ]) #Old model.
plot(svm.mmc.linear2, linearly.separable2) #New model.

#Additional information for the fit.
summary(svm.mmc.linear2)

#Finding the indices of the support vectors.
svm.mmc.linear2$index



###################################
#####Support Vector Classifier#####
###################################
#Fitting a support vector classifier by reducing the cost of a misclassified
#observation.
svm.svc.linear2 = svm(y ~ .,
                      data = linearly.separable2,
                      kernel = "linear",
                      cost = 1)

#Visualizing the results of the support vector classifier.
plot(svm.svc.linear2, linearly.separable2)
summary(svm.svc.linear2)
svm.svc.linear2$index

#What happens if we reduce the cost even more?
svm.svc.linear3 = svm(y ~ .,
                      data = linearly.separable2,
                      kernel = "linear",
                      cost = .1)
plot(svm.svc.linear3, linearly.separable2)
summary(svm.svc.linear3)
svm.svc.linear3$index

#We generally find the best cost parameter by implementing the cross-validation
#procedure; this isn't as interesting with linearly separable data. Let's generate
#some data that is not linearly separable.
set.seed(0)
x1 = c(rnorm(100, -1, 1), rnorm(100, 1, 1))
x2 = c(rnorm(100, -1, 1), rnorm(100, 1, 1))
y = as.factor(c(rep(-1, 100), rep(1, 100)))
overlapping = data.frame(x1, x2, y)
plot(overlapping$x1, overlapping$x2, col = overlapping$y)

#Implement cross-validation to select the best parameter value of the cost.
set.seed(0)
cv.svm.overlapping = tune(svm,
                          y ~ .,
                          data = overlapping[train.index, ],
                          kernel = "linear",
                          ranges = list(cost = 10^(seq(-5, .5, length = 100))))

#Inspecting the cross-validation output.
summary(cv.svm.overlapping)

#Plotting the cross-validation results.
plot(cv.svm.overlapping$performances$cost,
     cv.svm.overlapping$performances$error,
     xlab = "Cost",
     ylab = "Error Rate",
     type = "l")

#Inspecting the best model.
best.overlapping.model = cv.svm.overlapping$best.model
summary(best.overlapping.model)

#Using the best model to predict the test data.
ypred = predict(best.overlapping.model, overlapping[test.index, ])
table("Predicted Values" = ypred, "True Values" = overlapping[test.index, "y"])

#Constructing and visualizing the final model.
svm.best.overlapping = svm(y ~ .,
                           data = overlapping,
                           kernel = "linear",
                           cost = best.overlapping.model$cost)
plot(svm.best.overlapping, overlapping)
summary(svm.best.overlapping)
svm.best.overlapping$index
ypred = predict(svm.best.overlapping, overlapping)
table("Predicted Values" = ypred, "True Values" = overlapping[, "y"])



#################################
#####Support Vector Machines#####
#################################
#What happens if we have data that is not linearly separable?
set.seed(0)
x1 = c(rnorm(100, 2), rnorm(100, -2), rnorm(100))
x2 = c(rnorm(100, 2), rnorm(100, -2), rnorm(100))
y = as.factor(c(rep(-1, 200), rep(1, 100)))
nonlinear = data.frame(x1, x2, y)
plot(nonlinear$x1, nonlinear$x2, col = nonlinear$y)

#A linear kernel will fail in this scenario. Let's try using a radial kernel.
svm.radial = svm(y ~ .,
                 data = nonlinear,
                 kernel = "radial",
                 cost = 1,
                 gamma = .5) #Default is 1/p.

#Visualizing the results of the support vector machine
plot(svm.radial, nonlinear)
summary(svm.radial)
svm.radial$index

#What happens if we make gamma small?
svm.radial.smallgamma = svm(y ~ .,
                            data = nonlinear,
                            kernel = "radial",
                            cost = 1,
                            gamma = .05)
plot(svm.radial.smallgamma, nonlinear)
summary(svm.radial.smallgamma)
svm.radial.smallgamma$index

#What happens if we make gamma large?
svm.radial.largegamma = svm(y ~ .,
                            data = nonlinear,
                            kernel = "radial",
                            cost = 1,
                            gamma = 10)
plot(svm.radial.largegamma, nonlinear)
summary(svm.radial.largegamma)
svm.radial.largegamma$index

#Let's use cross-validation to figure out the best combination of the tuning
#parameters.

#Creating training and test sets.
set.seed(0)
train.index = sample(1:300, 300*.8)
test.index = -train.index

#Performing the cross-validation.
#CAUTION: Will take about 30 seconds.
set.seed(0)
cv.svm.radial = tune(svm,
                     y ~ .,
                     data = nonlinear[train.index, ],
                     kernel = "radial",
                     ranges = list(cost = 10^(seq(-1, 1.5, length = 20)),
                                   gamma = 10^(seq(-2, 1, length = 20))))

#Inspecting the cross-validation output.
summary(cv.svm.radial)

#Plotting the cross-validation results.
library(rgl)
plot3d(cv.svm.radial$performances$cost,
       cv.svm.radial$performances$gamma,
       cv.svm.radial$performances$error,
       xlab = "Cost",
       ylab = "Gamma",
       zlab = "Error",
       type = "s",
       size = 1)

#Inspecting the best model.
best.nonlinear.model = cv.svm.radial$best.model
summary(best.nonlinear.model)

#Using the best model to predict the test data.
ypred = predict(best.nonlinear.model, nonlinear[test.index, ])
table("Predicted Values" = ypred, "True Values" = nonlinear[test.index, "y"])

#Constructing and visualizing the final model.
svm.best.nonlinear = svm(y ~ .,
                         data = nonlinear,
                         kernel = "radial",
                         cost = best.nonlinear.model$cost,
                         gamma = best.nonlinear.model$gamma)
plot(svm.best.nonlinear, nonlinear)
summary(svm.best.nonlinear)
svm.best.nonlinear$index
ypred = predict(svm.best.nonlinear, nonlinear)
table("Predicted Values" = ypred, "True Values" = nonlinear[, "y"])



########################################
#####Multi-Class SVM Classification#####
########################################
#Creating multi-class data.
set.seed(0)
x1 = c(rnorm(100, 2), rnorm(100, -2), rnorm(100), rnorm(100, 2))
x2 = c(rnorm(100, 2), rnorm(100, -2), rnorm(100), rnorm(100, -2))
y = as.factor(c(rep(-1, 200), rep(1, 100), rep(2, 100)))
multi = data.frame(x1, x2, y)
plot(multi$x1, multi$x2, col = multi$y)

#Creating training and test sets.
set.seed(0)
train.index = sample(1:400, 400*.8)
test.index = -train.index

#Performing the cross-validation.
#CAUTION: Will take about 45 seconds.
set.seed(0)
cv.multi = tune(svm,
                y ~ .,
                data = multi[train.index, ],
                kernel = "radial",
                ranges = list(cost = 10^(seq(-1, 1.5, length = 20)),
                              gamma = 10^(seq(-2, 1, length = 20))))

#Inspecting the cross-validation output.
summary(cv.multi)

#Plotting the cross-validation results.
plot3d(cv.multi$performances$cost,
       cv.multi$performances$gamma,
       cv.multi$performances$error,
       xlab = "Cost",
       ylab = "Gamma",
       zlab = "Error",
       type = "s",
       size = 1)

#Inspecting the best model.
best.multi.model = cv.multi$best.model
summary(best.multi.model)

#Using the best model to predict the test data.
ypred = predict(best.multi.model, multi[test.index, ])
table("Predicted Values" = ypred, "True Values" = multi[test.index, "y"])

#Constructing and visualizing the final model.
svm.best.multi = svm(y ~ .,
                     data = multi,
                     kernel = "radial",
                     cost = best.multi.model$cost,
                     gamma = best.multi.model$gamma)
plot(svm.best.multi, multi)
summary(svm.best.multi)
svm.best.multi$index
ypred = predict(svm.best.multi, multi)
table("Predicted Values" = ypred, "True Values" = multi[, "y"])