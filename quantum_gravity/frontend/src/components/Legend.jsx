export default function Legend() {
  return (
    <div className="legend">
      <h2>Legend</h2>
      <ul>
        <li>
          <span className="legend-swatch legend-dot" aria-hidden="true" />
          <div>
            <strong>Boundary</strong>
            <span>6 qubits on the outer circle — where the "quantum system" lives.</span>
          </div>
        </li>
        <li>
          <span className="legend-swatch legend-polygon" aria-hidden="true" />
          <div>
            <strong>Bulk</strong>
            <span>The interior geometry, emergent from boundary entanglement.</span>
          </div>
        </li>
        <li>
          <span className="legend-swatch legend-line" aria-hidden="true" />
          <div>
            <strong>Entanglement entropy</strong>
            <span>Edge glow and thickness — more entangled boundary pairs shine brighter.</span>
          </div>
        </li>
      </ul>
    </div>
  );
}
