import { useState } from "react";
import { useNavigate } from "react-router-dom";

function LearningDetails() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const skill =
    localStorage.getItem("selectedSkill") ||
    "Learning Skill";

  const career =
    localStorage.getItem("normalizedCareer") ||
    localStorage.getItem("learningGoal") ||
    "";

  const handleComplete = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `http://localhost:8000/api/progress/1/complete?skill=${encodeURIComponent(
          skill
        )}&career=${encodeURIComponent(career)}`,
        {
          method: "POST"
        }
      );

      if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
          errorData.detail ||
            "Could not mark skill as completed."
        );
      }

      const data = await response.json();

      // Save the latest progress locally too.
      localStorage.setItem(
        "progressData",
        JSON.stringify(data)
      );

      // Go back to roadmap so it fetches the
      // latest progress from the backend.
      navigate("/roadmap");
    } catch (error) {
      console.error(error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>{skill}</h1>

      <h2>Why should you learn this?</h2>

      <p>
        Learning {skill} will help you progress
        toward your goal of becoming a{" "}
        {career || "professional"}.
      </p>

      <h2>Topics to Learn</h2>

      <ul>
        <li>Understand the fundamentals</li>
        <li>Practice the important concepts</li>
        <li>Complete exercises and examples</li>
        <li>Build something using this skill</li>
      </ul>

      <h2>Recommended Practice</h2>

      <p>
        Practice {skill} by completing a small
        project related to your career goal.
      </p>

      {error && (
        <p style={{ color: "red" }}>
          {error}
        </p>
      )}

      <button
        onClick={() => navigate("/roadmap")}
        disabled={loading}
      >
        Back to Roadmap
      </button>

      <button
        onClick={handleComplete}
        disabled={loading}
      >
        {loading
          ? "Saving..."
          : "Mark as Completed"}
      </button>
    </div>
  );
}

export default LearningDetails;