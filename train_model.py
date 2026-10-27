import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,r2_score
import joblib
from pathlib import Path


#1.Create a sample dataset as :
data ={
    "hours_studied": [1,2,3,4,5,6,7,8,2,4,6,8,3,5,7,9,1,5,6,9],
    "attendance" :   [50, 55, 60, 65, 70, 75, 80, 90, 60, 70,85, 95, 65, 75, 85, 95, 45, 80, 70, 98],
    "previous_score":[40, 45, 50, 55, 60, 65, 70, 80, 48, 58,68, 82, 52, 62, 72, 85, 35, 65, 75, 90],
    "final_score":   [42, 46, 53, 56, 63, 68, 74, 86, 49, 60,72, 88, 54, 65, 77, 91, 37, 67, 76, 94]

}

df = pd.DataFrame(data)


#2.Separate features x and target variables y

x=df[['hours_studied','attendance','previous_score']]
y=df['final_score']


#3.Split the data into training and testing sets

X_train,X_test,Y_train,Y_test = train_test_split(x,y,test_size = 0.2,random_state=42)


#4.Train the model according to the data

model = LinearRegression()
model.fit(X_train,Y_train)

#5. predict the model
prediction = model.predict(X_test)

#6.Find out the results
print("Mean Absolute Error:",mean_absolute_error(Y_test,prediction))
print("R2 score:",r2_score(Y_test,prediction))


#7.save the trained model
model_path = Path(__file__).parent / "model" /"student_score_model.joblib"
joblib.dump(model,model_path)

print(f"MOdel saved to : {model_path}")