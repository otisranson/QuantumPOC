export default function ModeToggle({ mode, onChange }) {
  const isQuantum = mode === "quantum";
  return (
    <div className="mode-toggle" role="radiogroup" aria-label="Geometry source">
      <button
        type="button"
        role="radio"
        aria-checked={isQuantum}
        className={isQuantum ? "active" : ""}
        onClick={() => onChange("quantum")}
      >
        Quantum entanglement
      </button>
      <button
        type="button"
        role="radio"
        aria-checked={!isQuantum}
        className={!isQuantum ? "active" : ""}
        onClick={() => onChange("classical")}
      >
        Classical random graph
      </button>
    </div>
  );
}
