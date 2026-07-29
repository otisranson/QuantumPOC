import { useCallback, useEffect, useRef, useState } from "react";
import FieldCanvas from "./components/FieldCanvas.jsx";
import ControlPanel from "./components/ControlPanel.jsx";
import Caption from "./components/Caption.jsx";
import { fetchField, fetchLearned } from "./api.js";
import { HBAR_DEFAULT, NUM_PATHS_DEFAULT } from "./constants.js";
import { useDebouncedCallback } from "./useDebouncedCallback.js";

export default function App() {
  const [start, setStart] = useState([-0.6, 0]);
  const [end, setEnd] = useState([0.6, 0]);
  const [hbar, setHbar] = useState(HBAR_DEFAULT);
  const [numPaths, setNumPaths] = useState(NUM_PATHS_DEFAULT);
  const [mode, setMode] = useState("computed");
  const [field, setField] = useState(null);
  const [error, setError] = useState(null);
  const requestId = useRef(0);

  const load = useCallback(async (currentStart, currentEnd, currentNumPaths, currentHbar, currentMode) => {
    const id = ++requestId.current;
    try {
      const data =
        currentMode === "computed"
          ? await fetchField(currentStart, currentEnd, currentNumPaths, currentHbar)
          : await fetchLearned(currentStart, currentEnd, currentHbar);
      if (id === requestId.current) {
        setField(data.field);
        setError(null);
      }
    } catch (err) {
      if (id === requestId.current) setError(err.message);
    }
  }, []);

  const debouncedLoad = useDebouncedCallback(load, 100);

  useEffect(() => {
    debouncedLoad(start, end, numPaths, hbar, mode);
  }, [start, end, numPaths, hbar, mode, debouncedLoad]);

  return (
    <div className="app">
      <FieldCanvas field={field} start={start} end={end} onStartChange={setStart} onEndChange={setEnd} />
      <ControlPanel
        hbar={hbar}
        onHbarChange={setHbar}
        numPaths={numPaths}
        onNumPathsChange={setNumPaths}
        mode={mode}
        onModeChange={setMode}
      />
      <Caption />
      {error && <p className="error-banner">{error}</p>}
    </div>
  );
}
