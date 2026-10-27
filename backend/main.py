from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware

from schemas import StudentPredictionInput, StudentPredictionOutput


app = FastAPI(title='Student Score Predictor API')

#Allow requests from our local React development server
#allows the communication between the react(javascript) and python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers =["*"],
)

#Load the trained model once when the API starts.

MODEL_PATH =Path(__file__).parent/"model"/"student_score_model.joblib"
model = joblib.load(MODEL_PATH)

#shared dependency : Prepare input in the same format used during training.

def prepare_features(
        student:StudentPredictionInput,
) -> pd.DataFrame:
    return pd.DataFrame(
    [
            {
                "hours_studied": student.hours_studied,
                "attendance": student.attendance,
                "previous_score": student.previous_score,
            }
    ]
)

@app.get("/")
def home():
    return{"message":"Student score predictor API is running"}

@app.post(
    "/predict",response_model =StudentPredictionOutput,
) 

def predict_score(
    student : StudentPredictionInput,
    features : pd.DataFrame = Depends(prepare_features),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
):
    prediction = model.predict(features)[0]

    return {
        "predicted_score": round(
            float(max(0, min(100, prediction))), 2
        )
    }
    