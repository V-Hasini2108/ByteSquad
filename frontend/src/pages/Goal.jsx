import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Goal() {
  const navigate = useNavigate();
  const [goal, setGoal] = useState("");

  const handleContinue = () => {
    if (goal.trim() === "") {
      alert("Please enter your learning goal");
      return;
    }

    localStorage.setItem("learningGoal", goal);

    navigate("/profile");
  };

  return (
    <div className="page-container">
      <div className="form-card">
        <span className="step-text">
          STEP 1 OF 2
        </span>

        <h1>What do you want to achieve?</h1>

        <p>
          Describe your career or learning goal in your own words.
        </p>

        <textarea
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          placeholder="Example: I want to become a Java Full Stack Developer"
          rows="7"
        />

        <button
          className="primary-button"
          onClick={handleContinue}
        >
          Continue →
        </button>
      </div>
    </div>
  );
}

export default Goal;