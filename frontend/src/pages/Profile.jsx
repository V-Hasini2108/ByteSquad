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
    <div>
      <h1>Create Your Learning Profile</h1>

      <label>Current Skill Level</label>
      <br />

      <select
        value={level}
        onChange={(e) => setLevel(e.target.value)}
      >
        <option>Beginner</option>
        <option>Intermediate</option>
        <option>Advanced</option>
      </select>

      <br />
      <br />

      <label>Skills You Already Know</label>
      <br />

      <input
        type="text"
        value={skills}
        onChange={(e) => setSkills(e.target.value)}
        placeholder="Example: Java, Python, HTML"
      />

      <br />
      <br />

      <label>Study Hours Per Week</label>
      <br />

      <input
        type="number"
        value={studyHours}
        onChange={(e) => setStudyHours(e.target.value)}
        placeholder="Example: 10"
      />

      <br />
      <br />

      <label>Target Duration</label>
      <br />

      <select
        value={duration}
        onChange={(e) => setDuration(e.target.value)}
      >
        <option>1 Month</option>
        <option>3 Months</option>
        <option>6 Months</option>
        <option>1 Year</option>
      </select>

      <br />
      <br />

      <button onClick={handleSubmit}>
        Generate My Learning Path
      </button>
    </div>
  );
}

export default Profile;