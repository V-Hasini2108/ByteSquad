import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Roadmap() {
  const navigate = useNavigate();

  const [roadmapData, setRoadmapData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadRoadmap = async () => {
      try {
        const rawGoal =
          localStorage.getItem("learningGoal") || "";

        const profile = JSON.parse(
          localStorage.getItem("learnerProfile") || "{}"
        );

        const normalizeCareer = (input) => {
          const goal = input.toLowerCase().trim();

          // Frontend Developer
          if (
            goal.includes("frontend") ||
            goal.includes("front-end") ||
            goal.includes("front end")
          ) {
            return "Frontend Developer";
          }

          // Java Full Stack
          if (
            goal.includes("java") &&
            goal.includes("full stack")
          ) {
            return "Java Full Stack Developer";
          }

          // Python Full Stack
          if (
            goal.includes("python") &&
            goal.includes("full stack")
          ) {
            return "Python Full Stack Developer";
          }

          // Data Scientist
          if (
            goal.includes("data scientist") ||
            goal.includes("data science")
          ) {
            return "Data Scientist";
          }

          // Machine Learning Engineer
          if (
            goal.includes("machine learning") ||
            goal.includes("ml engineer")
          ) {
            return "Machine Learning Engineer";
          }

          // K-pop Idol
          if (
            goal.includes("k-pop") ||
            goal.includes("kpop") ||
            goal.includes("k pop") ||
            goal.includes("idol")
          ) {
            return "K-pop Idol";
          }

          // Singer
          if (
            goal.includes("singer") ||
            goal.includes("singing") ||
            goal.includes("vocalist") ||
            goal.includes("sing")
          ) {
            return "Singer";
          }

          // Dancer
          if (
            goal.includes("dancer") ||
            goal.includes("dancing") ||
            goal.includes("dance")
          ) {
            return "Dancer";
          }

          // If no match is found, send the original goal.
          return input.trim();
        };

        const goal = normalizeCareer(rawGoal);

        if (!goal) {
          setError("Learning goal not found.");
          setLoading(false);
          return;
        }

        const currentSkills = profile.skills
          ? profile.skills
              .split(",")
              .map((skill) => skill.trim())
              .filter(Boolean)
          : [];

        const response = await fetch(
          "http://localhost:8000/api/roadmap",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              learnerId: 1,
              career: goal,
              currentSkills
            })
          }
        );

        if (!response.ok) {
          const errorData = await response.json();

          throw new Error(
            errorData.detail ||
              "Could not generate roadmap."
          );
        }

        const data = await response.json();

        setRoadmapData(data);

        localStorage.setItem(
          "roadmapData",
          JSON.stringify(data)
        );

        localStorage.setItem(
          "normalizedCareer",
          goal
        );
      } catch (error) {
        console.error(error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    loadRoadmap();
  }, []);

  if (loading) {
    return (
      <div>
        <h2>
          Generating your personalized roadmap...
        </h2>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <h2>Unable to generate roadmap</h2>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Your Personalized Learning Roadmap</h1>

      <h2>
        Goal: {roadmapData.career}
      </h2>

      <h3>
        Progress: {roadmapData.progressPercentage}%
      </h3>

      <p>
        Completed:{" "}
        {roadmapData.completedSkills.length} /{" "}
        {roadmapData.totalSkills}
      </p>

      {roadmapData.roadmap.map((item) => (
        <div
          key={item.phase}
          onClick={() => {
            localStorage.setItem(
              "selectedSkill",
              item.skill
            );

            navigate("/learning-details");
          }}
          style={{
            marginBottom: "20px",
            padding: "15px",
            border: "1px solid #ccc",
            borderRadius: "10px",
            cursor: "pointer"
          }}
        >
          <h3>
            Phase {item.phase}: {item.skill}
          </h3>

          <p>{item.milestone}</p>

          <p>
            Status: {item.status}
          </p>
        </div>
      ))}

      <button
        onClick={() => navigate("/dashboard")}
      >
        View Progress Dashboard
      </button>
    </div>
  );
}

export default Roadmap;