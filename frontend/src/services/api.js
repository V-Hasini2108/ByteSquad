const API_URL = "http://localhost:8000";

export async function generateRoadmap(userData) {
  const response = await fetch(
    `${API_URL}/api/roadmap`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(userData)
    }
  );

  return response.json();
}