import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="page-container home-page">
      <div className="hero-card">
        <span className="ai-badge">AI-Powered Learning</span>

        <h1>
          Build Your Personalized
          <br />
          Learning Journey
        </h1>

        <p>
          Tell us your goal, skills and learning preferences.
          Our AI helps create a structured learning path
          designed specifically for you.
        </p>

        <button
          className="primary-button"
          onClick={() => navigate("/goal")}
        >
          Start Your Learning Journey →
        </button>
      </div>
    </div>
  );
}

export default Home;