from sklearn.preprocessing import MinMaxScaler
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
# Our self defined ML model
import model as solarModel

df = pd.read_csv('daytime_readings.csv')


def process_power_attributes(df, train, test):
    # initialize the column names of the continuous data
    continuous = ["SolIrr", "TmpAmb", "TmpMod", "Wind"]
    # performing min-max scaling each continuous feature column to the range [0, 1]
    cs = MinMaxScaler()
    trainContinuous = cs.fit_transform(train[continuous])
    testContinuous = cs.transform(test[continuous])

    return trainContinuous, testContinuous


# construct a training and testing split with 75% of the data used for training and the remaining 25% for evaluation
print("[INFO] constructing training/testing split...")
(train, test) = train_test_split(df, test_size=0.25, random_state=42)

'''
find the largest Pdc in the training set and use it to scale our Pdcs to the range [0, 1] 
(this will lead to better training and convergence)
'''
maxPdc = train["Pdc"].max()
trainY = train["Pdc"] / maxPdc
testY = test["Pdc"] / maxPdc

# process the power attributes data by performing min-max scaling on continuous features
print("[INFO] processing data...")
(trainX, testX) = process_power_attributes(df, train, test)

'''
create our MLP and then compile the model using mean absolute percentage error as our loss, implying that we seek to 
minimize the absolute percentage difference between our PDC *predictions* and the *actual PDCs*
'''
model = solarModel.create_mlp(trainX.shape[1], regress=True)
opt = Adam(lr=1e-3, decay=1e-3 / 200)
model.compile(loss="mean_absolute_percentage_error", optimizer=opt)

# train the model
print("[INFO] training model...")
model.fit(trainX, trainY, validation_data=(testX, testY), epochs=200, batch_size=8)

# make predictions on the testing data
print("[INFO] predicting PDC values...")
preds = model.predict(testX)

'''
compute the difference between the *predicted* PDCs and the *actual* PDCs, 
then compute the percentage difference and the absolute percentage difference
'''
diff = preds.flatten() - testY
percentDiff = (diff / testY) * 100
absPercentDiff = np.abs(percentDiff)

# compute the mean and standard deviation of the absolute percentage difference
mean = np.mean(absPercentDiff)
std = np.std(absPercentDiff)

# finally, show some statistics on our model
print("[INFO] avg. PDC: {}, std PDC: {}".format(df["Pdc"].mean(), df["Pdc"].std()))
print("[INFO] mean: {:.2f}%, std: {:.2f}%".format(mean, std))
