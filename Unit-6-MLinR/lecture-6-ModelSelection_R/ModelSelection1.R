
# Slide 7
set.seed(0); x = seq(-2, 5, length=100)
noise = rnorm(100); y = 3 + 2*x^2 + 4*noise
plot(x, y)

# Slide 8
plot(x, y)
model1 = lm(y ~ x)
abline(model1)

# Slide 9
model2 = lm(y ~ poly(x,20))
plot(x, y)
lines(x, model2$fitted.values)

# Slide 11
dat = data.frame(x,y)
set.seed(1)
index = sample(1:100, 50)
train = dat[index,]
test = dat[-index,]

# Slide 12
rmse_train = function(n) {
  model = lm(y ~ poly(x,n), data=train)
  pred = predict(model)
  rmse = sqrt(mean((train$y-pred)^2))
  return(rmse)
}
rmse1 = sapply(1:10, rmse_train)
plot(1:10, rmse1, type='b')

# Slide 14
rmse_test = function(n) {
  model = lm(y ~ poly(x, n), data=train)
  pred = predict(model, newdata=test)
  rmse = sqrt(mean((test$y-pred)^2))
  return(rmse) 
}
rmse2 = sapply(1:10, rmse_test)

# Slide 16
plotdata = data.frame(rmse=c(rmse1,rmse2),
                      type=rep(c('train','test'), each=10),
                      x=rep(1:10,times=2))
library(ggplot2)
p = ggplot(plotdata, aes(x=x,y=rmse,group=type,color=type))
p = p + geom_point() + geom_line()

y = c(rep('a', 9990), rep('b', 10))
set.seed(2)
index = sample(1:10000, size= 7000)
label_train = y[index]
label_test = y[-index]
print(mean(label_train=='b'))
print(mean(label_test=='b'))

# Slide 20
credit = read.csv("./data/credit.csv")
View(credit)


# Slide 21
set.seed(0)
index = sample(1:nrow(credit), size= nrow(credit)*0.7)
### Training
logit = glm(default~., data = credit[index, ], family = 'binomial')
### Testing
prob = predict(logit, credit[-index, ], type="response")
mean((prob>=0.5) == (credit$default[-index]=='yes'))

# Slide 23
y = c(rep('a', 9990), rep('b', 10))
set.seed(2)
index = sample(1:10000, size= 7000)
label_train = y[index]
label_test = y[-index]
print(mean(label_train=='b'))
print(mean(label_test=='b'))

# Slide 25
library(caret)
folds = createFolds(credit$default, 5)
str(folds)


# Slide 27
n=5
accuracy = numeric(n)
for(i in 1:n){
  index = -folds[[i]]
  logit = glm(default~., data = credit[index, ],
              family = 'binomial')
  prob = predict(logit, credit[-index, ], type="response")
  accuracy[i] = mean(
    (prob>=0.5) == (credit$default[-index]=='yes')
  )
}
accuracy


# Slide 28
print(mean(accuracy)); print(sd(accuracy))


# Slide 29
ctrl = trainControl(method = "cv", number = 5)
logit_cv = train(default ~ ., data=credit,
                 method = "glm", trControl = ctrl)
logit_cv$results


# Slide 31
ctrl = trainControl(method = "cv", number = 5)
tune.grid = expand.grid(lambda = (0:10)*0.1, alpha=0)
logit_shrinkage = train(default ~ ., data=credit, method = "glmnet",
                        metric = "Accuracy", trControl = ctrl,
                        preProc=c('center', 'scale'), tuneGrid = tune.grid)
logit_shrinkage$results

# Slide 34
set.seed(0)
index = sample(1:nrow(credit), size= nrow(credit)*0.8)
train_data = credit[index, ]
test_data = credit[-index, ]
tune.grid = expand.grid(lambda = (0:10)*0.1, alpha=0)
ctrl = trainControl(method = "repeatedcv", number = 5, repeats = 5)
logit_shrinkage = train(default ~ ., data=train_data,
                        method = "glmnet", metric = "Accuracy",
                        preProc=c('center', 'scale'),
                        trControl = ctrl, tuneGrid = tune.grid)


# Slide 35
logit_shrinkage$bestTune

# Slide 36
mean(predict.train(logit_shrinkage, test_data)==test_data$default)






