import { useState } from "react";
import { useNavigate } from "react-router-dom";

const API_URL = "http://localhost:8000";

function normalizeGoal(goal) {
  const text = goal.toLowerCase().trim();

  // Frontend Developer
  if (
    text.includes("frontend") ||
    text.includes("front-end") ||
    text.includes("front end")
  ) {
    return "Frontend Developer";
  }

  // Java Full Stack Developer
  if (
    text.includes("java") &&
    (
      text.includes("developer") ||
      text.includes("development") ||
      text.includes("full stack") ||
      text.includes("full-stack")
    )
  ) {
    return "Java Full Stack Developer";
  }

  // Python Full Stack Developer
  if (
    text.includes("python") &&
    (
      text.includes("developer") ||
      text.includes("development") ||
      text.includes("full stack") ||
      text.includes("full-stack")
    )
  ) {
    return "Python Full Stack Developer";
  }

  // Data Scientist
  if (
    text.includes("data scientist") ||
    text.includes("data science")
  ) {
    return "Data Scientist";
  }

  // Machine Learning Engineer
  if (
    text.includes("machine learning") ||
    text.includes("ml engineer")
  ) {
    return "Machine Learning Engineer";
  }

  // K-pop Idol
  if (
    text.includes("k-pop") ||
    text.includes("kpop") ||
    text.includes("k pop") ||
    text.includes("idol")
  ) {
    return "K-pop Idol";
  }

  // Singer
  if (
    text.includes("singer") ||
    text.includes("singing") ||
    text.includes("vocalist") ||
    text.includes("vocal")
  ) {
    return "Singer";
  }

  // Dancer
  if (
    text.includes("dancer") ||
    text.includes("dancing") ||
    text.includes("dance")
  ) {
    return "Dancer";
  }

  // Content Creator
  if (
    text.includes("content creator") ||
    text.includes("content creation") ||
    text.includes("youtuber") ||
    text.includes("youtube creator")
  ) {
    return "Content Creator";
  }

  // Graphic Designer
  if (
    text.includes("graphic designer") ||
    text.includes("graphic design") ||
    text.includes("designing")
  ) {
    return "Graphic Designer";
  }

  return null;
}

function Profile() {
  const navigate = useNavigate();

  const [level, setLevel] = useState("Beginner");
  const [skills, setSkills] = useState("");
  const [studyHours, setStudyHours] = useState("");
  const [duration, setDuration] = useState("3 Months");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (skills.trim() === "" || studyHours === "") {
      alert("Please fill all required fields");
      return;
    }

    const goal = localStorage.getItem("learningGoal");

    if (!goal) {
      alert("Please enter your learning goal first.");
      navigate("/goal");
      return;
    }

    const career = normalizeGoal(goal);

    if (!career) {
      alert(
        "We could not identify that career yet. Try Frontend Developer, Singer, Dancer, K-pop Idol, Content Creator or Graphic Designer."
      );
      return;
    }

    setLoading(true);

    try {
      // -----------------------------------------
      // STEP 1: Create learner profile
      // -----------------------------------------

      const profileResponse = await fetch(
        `${API_URL}/api/profile`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            goal: goal,
            skillLevel: level,
            skills: skills,
            studyHours: Number(studyHours),
            duration: duration
          })
        }
      );

      if (!profileResponse.ok) {
        const errorText = await profileResponse.text();
        throw new Error(
          `Profile creation failed: ${errorText}`
        );
      }

      const profileData = await profileResponse.json();

      // -----------------------------------------
      // STEP 2: Convert skills into an array
      // -----------------------------------------

      const currentSkills = skills
        .split(",")
        .map((skill) => skill.trim())
        .filter((skill) => skill !== "");

      // -----------------------------------------
      // STEP 3: Generate personalized roadmap
      // -----------------------------------------

      const roadmapResponse = await fetch(
        `${API_URL}/api/roadmap`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            learnerId: profileData.id,
            career: career,
            currentSkills: currentSkills
          })
        }
      );

      if (!roadmapResponse.ok) {
        const errorText = await roadmapResponse.text();
        throw new Error(
          `Roadmap generation failed: ${errorText}`
        );
      }

      const roadmapData = await roadmapResponse.json();

      // -----------------------------------------
      // STEP 4: Save everything for Roadmap.jsx
      // -----------------------------------------

      localStorage.setItem(
        "learnerProfile",
        JSON.stringify(profileData)
      );

      localStorage.setItem(
        "roadmapData",
        JSON.stringify(roadmapData)
      );

      localStorage.setItem(
        "selectedCareer",
        career
      );

      // -----------------------------------------
      // STEP 5: Open roadmap
      // -----------------------------------------

      navigate("/roadmap");

    } catch (error) {
      console.error("Error generating roadmap:", error);

      alert(
        "Something went wrong while generating your learning path. Please make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
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
            placeholder="Example: HTML, CSS, Python"
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
          disabled={loading}
        >
          {loading
            ? "Generating..."
            : "Generate My Learning Path ✨"}
        </button>

      </div>
    </div>
  );
}

export default Profile;