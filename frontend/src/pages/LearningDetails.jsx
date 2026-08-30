import { useNavigate } from "react-router-dom";

function LearningDetails() {
  const navigate = useNavigate();

  return (
    <div>
      <h1>Object-Oriented Programming</h1>

      <h2>Why should you learn this?</h2>

      <p>
        Object-Oriented Programming is an important
        foundation for building large Java applications.
      </p>

      <h2>Topics to Learn</h2>

      <ul>
        <li>Classes and Objects</li>
        <li>Inheritance</li>
        <li>Polymorphism</li>
        <li>Encapsulation</li>
        <li>Abstraction</li>
      </ul>

      <h2>Recommended Project</h2>

      <p>Build a Student Management System.</p>

      <button onClick={() => navigate("/roadmap")}>
        Back to Roadmap
      </button>

      <button onClick={() => navigate("/dashboard")}>
        Mark as Completed
      </button>
    </div>
  );
}

export default LearningDetails;