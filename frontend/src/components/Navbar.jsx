import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav>
      <h2>LearnPath AI</h2>

      <div>
        <Link to="/">Home</Link>
        {" | "}
        <Link to="/roadmap">Roadmap</Link>
        {" | "}
        <Link to="/dashboard">Dashboard</Link>
      </div>
    </nav>
  );
}

export default Navbar;