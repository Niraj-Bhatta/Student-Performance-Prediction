
import { useState } from "react";
import "./App.css";

const initialForm = {
  hours_studied: "",
  attendance: "",
  previous_score: "",
};

function App() {
  const [form, setForm] = useState(initialForm);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));

    setPrediction(null);
    setError("");
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setPrediction(null);
    setError("");

    const hours = Number(form.hours_studied);
    const attendance = Number(form.attendance);
    const previousScore = Number(form.previous_score);

    if (
      form.hours_studied === "" ||
      form.attendance === "" ||
      form.previous_score === ""
    ) {
      setError("Please fill in all fields.");
      return;
    }

    if (!Number.isFinite(hours) || hours < 0 || hours > 24) {
      setError("Study hours must be between 0 and 24.");
      return;
    }

    if (
      !Number.isFinite(attendance) ||
      attendance < 0 ||
      attendance > 100
    ) {
      setError("Attendance must be between 0 and 100.");
      return;
    }

    if (
      !Number.isFinite(previousScore) ||
      previousScore < 0 ||
      previousScore > 100
    ) {
      setError("Previous score must be between 0 and 100.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          hours_studied: hours,
          attendance,
          previous_score: previousScore,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail?.[0]?.msg || "Prediction failed.");
      }

      setPrediction(data.predicted_score);
    } catch (err) {
      setError(
        err.message ||
          "Cannot connect to the API. Make sure the FastAPI server is running."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="predictor">
        <p className="eyebrow">MACHINE LEARNING PROJECT</p>
        <h1>Student Score Predictor</h1>
        <p className="subtitle">
          Enter your academic details to generate a predicted final score.
        </p>

        <form onSubmit={handleSubmit}>
          <label htmlFor="hours_studied">Study hours per day</label>
          <input
            id="hours_studied"
            name="hours_studied"
            type="number"
            min="0"
            max="24"
            step="any"
            placeholder="e.g. 6"
            value={form.hours_studied}
            onChange={handleChange}
          />

          <label htmlFor="attendance">Attendance (%)</label>
          <input
            id="attendance"
            name="attendance"
            type="number"
            min="0"
            max="100"
            step="any"
            placeholder="e.g. 85"
            value={form.attendance}
            onChange={handleChange}
          />

          <label htmlFor="previous_score">Previous score (out of 100)</label>
          <input
            id="previous_score"
            name="previous_score"
            type="number"
            min="0"
            max="100"
            step="any"
            placeholder="e.g. 70"
            value={form.previous_score}
            onChange={handleChange}
          />

          <button type="submit" disabled={loading}>
            {loading ? "Predicting..." : "Predict my score"}
          </button>
        </form>

        {error && (
          <div className="message error" role="alert">
            {error}
          </div>
        )}

        {prediction !== null && (
          <div className="result" aria-live="polite">
            <p>Predicted final score</p>
            <strong>{prediction.toFixed(2)} / 100</strong>
            <small>
              Educational demonstration only; not a reliable assessment of
              actual student performance.
            </small>
          </div>
        )}
      </section>
    </main>
  );
}

export default App;
