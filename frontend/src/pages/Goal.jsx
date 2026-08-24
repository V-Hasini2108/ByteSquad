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
    <div>
      <h1>What is your learning goal?</h1>

      <p>Tell us what you want to achieve.</p>

      <textarea
        value={goal}
        onChange={(e) => setGoal(e.target.value)}
        placeholder="Example: I want to become a Java Full Stack Developer"
        rows="6"
      />

      <br />
      <br />

      <button onClick={handleContinue}>
        Continue
      </button>
    </div>
  );
}

export default Goal;