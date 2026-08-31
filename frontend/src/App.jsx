import LearningDetails from "./pages/LearningDetails";
import Dashboard from "./pages/Dashboard";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import "./App.css";

import Home from "./pages/Home";
import Goal from "./pages/Goal";
import Profile from "./pages/Profile";
import Processing from "./pages/Processing";
import Roadmap from "./pages/Roadmap";

function App() {
  return (
    <>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/goal" element={<Goal />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/processing" element={<Processing />} />
        <Route path="/roadmap" element={<Roadmap />} />
        <Route
          path="/learning-details"
          element={<LearningDetails />}
        />
        <Route
          path="/dashboard"
          element={<Dashboard />}
        />
      </Routes>
    </>
  );
}

export default App;