import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Processing() {
  const navigate = useNavigate();

  const steps = [
    "Understanding your learning goal",
    "Analyzing your current skills",
    "Identifying skill gaps",
    "Creating your personalized roadmap"
  ];

  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((previous) => {
        if (previous < steps.length - 1) {
          return previous + 1;
        }

        clearInterval(interval);

        setTimeout(() => {
          navigate("/roadmap");
        }, 1000);

        return previous;
      });
    }, 1200);

    return () => clearInterval(interval);
  }, [navigate]);

  return (
    <div>
      <h1>Generating Your Personalized Learning Path</h1>

      <p>Please wait while our AI analyzes your profile.</p>

      {steps.map((step, index) => (
        <p key={index}>
          {index < currentStep && "✓ "}
          {index === currentStep && "⏳ "}
          {index > currentStep && "○ "}

          {step}
        </p>
      ))}
    </div>
  );
}

export default Processing;