import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Profile() {
  const navigate = useNavigate();

  const [level, setLevel] = useState("Beginner");
  const [skills, setSkills] = useState("");
  const [studyHours, setStudyHours] = useState("");
  const [duration, setDuration] = useState("3 Months");

  const handleSubmit = () => {
    if (skills.trim() === "" || studyHours === "") {
      alert("Please fill all required fields");
      return;
    }

    const profile = {
      level,
      skills,
      studyHours,
      duration
    };

    localStorage.setItem(
      "learnerProfile",
      JSON.stringify(profile)
    );

    navigate("/processing");
  };

  return (
    <div className="page-container">
      <div className="form-card">

        <span className="step-text">
          STEP 2 OF 2
        </span>

        <h1>Create Your Learning Profile</h1>

        <p>
          This helps us understand your current learning level.
        </p>

        <div className="form-group">
          <label>Current Skill Level</label>

          <select
            value={level}
            onChange={(e) => setLevel(e.target.value)}
          >
            <option>Beginner</option>
            <option>Intermediate</option>
            <option>Advanced</option>
          </select>
        </div>

        <div className="form-group">
          <label>Skills You Already Know</label>

          <input
            type="text"
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
            placeholder="Example: Java, HTML, Python"
          />
        </div>

        <div className="form-group">
          <label>Study Hours Per Week</label>

          <input
            type="number"
            value={studyHours}
            onChange={(e) => setStudyHours(e.target.value)}
            placeholder="Example: 10"
          />
        </div>

        <div className="form-group">
          <label>Target Duration</label>

          <select
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
          >
            <option>1 Month</option>
            <option>3 Months</option>
            <option>6 Months</option>
            <option>1 Year</option>
          </select>
        </div>

        <button
          className="primary-button"
          onClick={handleSubmit}
        >
          Generate My Learning Path ✨
        </button>

      </div>
    </div>
  );
}

export default Profile;