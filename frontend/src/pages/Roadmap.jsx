import { useNavigate } from "react-router-dom";

function Roadmap() {
  const navigate = useNavigate();

  const goal = localStorage.getItem("learningGoal");

  const roadmap = [
    {
      phase: "Phase 1",
      title: "Java Fundamentals",
      description: "Learn variables, loops, arrays and methods.",
      status: "completed"
    },
    {
      phase: "Phase 2",
      title: "Object-Oriented Programming",
      description: "Learn classes, objects, inheritance and polymorphism.",
      status: "current"
    },
    {
      phase: "Phase 3",
      title: "Java Collections",
      description: "Learn ArrayList, HashMap, Stack and Queue.",
      status: "locked"
    },
    {
      phase: "Phase 4",
      title: "SQL and Databases",
      description: "Learn database concepts and SQL queries.",
      status: "locked"
    },
    {
      phase: "Phase 5",
      title: "Spring Boot",
      description: "Build backend applications using Spring Boot.",
      status: "locked"
    },
    {
      phase: "Phase 6",
      title: "Final Project",
      description: "Build a complete project using your learned skills.",
      status: "locked"
    }
  ];

  return (
    <div>
      <h1>Your Personalized Learning Roadmap</h1>

      <h2>Goal: {goal}</h2>

      {roadmap.map((item, index) => (
        <div
          key={index}
          onClick={() => navigate("/learning-details")}
          style={{ marginBottom: "20px", cursor: "pointer" }}
        >
          <h3>
            {item.phase}: {item.title}
          </h3>

          <p>{item.description}</p>

          <p>Status: {item.status}</p>
        </div>
      ))}

      <button onClick={() => navigate("/dashboard")}>
        View Progress Dashboard
      </button>
    </div>
  );
}

export default Roadmap;