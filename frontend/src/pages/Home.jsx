import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  return (
    <div>
      <h1>LearnPath AI</h1>

      <p>
        AI-Powered Personalized Learning Path Recommender
      </p>

      <button onClick={() => navigate("/goal")}>
        Start Your Learning Journey
      </button>
    </div>
  );
}

export default Home;