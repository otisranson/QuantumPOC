export default function ExplanationPanel() {
  return (
    <div className="explanation-panel">
      <h2>What am I looking at?</h2>
      <p>
        This is a toy version of an idea from theoretical physics: that spacetime
        geometry itself might emerge from quantum entanglement, rather than being
        a fixed backdrop. Six qubits sit on the outer "boundary" circle; the
        sliders control how entangled each neighboring pair is. A real quantum
        circuit is simulated for every slider change, and the actual entanglement
        entropy is computed and used to push the interior "bulk" geometry
        outward, toward the boundary — more entanglement between boundary
        qubits swells the bulk outward, echoing how the Ryu-Takayanagi formula
        relates more entropy to a larger minimal surface; weak entanglement
        leaves the bulk collapsed toward the center. Toggle to the classical
        random graph to see that this structure isn't just a layout trick: it
        disappears without real quantum entanglement driving it.
      </p>
    </div>
  );
}
