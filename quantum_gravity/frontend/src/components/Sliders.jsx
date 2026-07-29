export default function Sliders({ strengths, onChange, disabled }) {
  return (
    <div className="sliders" aria-disabled={disabled}>
      <h2>Entanglement strength</h2>
      <p className="sliders-hint">
        One slider per ring edge. Because boundary qubits are shared between
        adjacent edges, a change can ripple around the whole ring.
      </p>
      {strengths.map((value, i) => (
        <label className="slider-row" key={i}>
          <span>
            Edge {i + 1}–{((i + 1) % strengths.length) + 1}
          </span>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={value}
            disabled={disabled}
            onChange={(event) => {
              const next = strengths.slice();
              next[i] = Number(event.target.value);
              onChange(next);
            }}
          />
          <span className="slider-value">{value.toFixed(2)}</span>
        </label>
      ))}
    </div>
  );
}
