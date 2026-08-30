function Dashboard() {
  const goal = localStorage.getItem("learningGoal");

  const completedSkills = [
    "Java Fundamentals"
  ];

  const currentSkill =
    "Object-Oriented Programming";

  const nextSkill =
    "Java Collections";

  const progress = 20;

  return (
    <div>
      <h1>Your Learning Dashboard</h1>

      <h2>Goal: {goal}</h2>

      <h2>Overall Progress: {progress}%</h2>

      <div
        style={{
          width: "400px",
          height: "20px",
          border: "1px solid black"
        }}
      >
        <div
          style={{
            width: `${progress}%`,
            height: "100%",
            backgroundColor: "blue"
          }}
        />
      </div>

      <h2>Completed Skills</h2>

      <ul>
        {completedSkills.map((skill, index) => (
          <li key={index}>✓ {skill}</li>
        ))}
      </ul>

      <h2>Currently Learning</h2>

      <p>→ {currentSkill}</p>

      <h2>Next Recommended Action</h2>

      <p>→ Learn {nextSkill}</p>
    </div>
  );
}

export default Dashboard;