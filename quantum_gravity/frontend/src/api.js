export async function fetchGeometry(strengths) {
  const res = await fetch("/api/geometry", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ strengths }),
  });
  if (!res.ok) throw new Error(`geometry request failed: ${res.status}`);
  return res.json();
}

export async function fetchBaseline(seed) {
  const res = await fetch(`/api/baseline?seed=${seed}`);
  if (!res.ok) throw new Error(`baseline request failed: ${res.status}`);
  return res.json();
}
