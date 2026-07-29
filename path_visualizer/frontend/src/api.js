export async function fetchField(start, end, numPaths, hbar) {
  const res = await fetch("/api/field", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ start, end, num_paths: numPaths, hbar }),
  });
  if (!res.ok) throw new Error(`field request failed: ${res.status}`);
  return res.json();
}

export async function fetchLearned(start, end, hbar) {
  const res = await fetch("/api/learned", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ start, end, hbar }),
  });
  if (!res.ok) throw new Error(`learned request failed: ${res.status}`);
  return res.json();
}
