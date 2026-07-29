import { useCallback, useEffect, useRef, useState } from "react";
import GeometryCanvas from "./components/GeometryCanvas.jsx";
import Sliders from "./components/Sliders.jsx";
import ModeToggle from "./components/ModeToggle.jsx";
import Legend from "./components/Legend.jsx";
import ExplanationPanel from "./components/ExplanationPanel.jsx";
import { fetchGeometry, fetchBaseline } from "./api.js";
import { NUM_QUBITS } from "./constants.js";
import { useDebouncedCallback } from "./useDebouncedCallback.js";

const SEED = 42;

export default function App() {
  const [strengths, setStrengths] = useState(() => Array(NUM_QUBITS).fill(0.5));
  const [mode, setMode] = useState("quantum");
  const [geometry, setGeometry] = useState(null);
  const [error, setError] = useState(null);
  const requestId = useRef(0);

  const load = useCallback(async (currentStrengths, currentMode) => {
    const id = ++requestId.current;
    try {
      const data =
        currentMode === "quantum"
          ? await fetchGeometry(currentStrengths)
          : await fetchBaseline(SEED);
      if (id === requestId.current) {
        setGeometry(data);
        setError(null);
      }
    } catch (err) {
      if (id === requestId.current) setError(err.message);
    }
  }, []);

  const debouncedLoad = useDebouncedCallback(load, 150);

  useEffect(() => {
    debouncedLoad(strengths, mode);
  }, [strengths, mode, debouncedLoad]);

  return (
    <div className="app">
      <header className="app-header">
        <h1>Quantum Gravity POC</h1>
        <p>Emergent bulk geometry from a toy HaPPY code, simulated with Qiskit.</p>
      </header>

      <main className="app-main">
        <div className="hero-panel">
          <ModeToggle mode={mode} onChange={setMode} />
          <GeometryCanvas geometry={geometry} />
          {error && <p className="error-banner">{error}</p>}
        </div>

        <aside className="side-panel">
          <Sliders
            strengths={strengths}
            onChange={setStrengths}
            disabled={mode !== "quantum"}
          />
          <Legend />
          <ExplanationPanel />
        </aside>
      </main>
    </div>
  );
}
