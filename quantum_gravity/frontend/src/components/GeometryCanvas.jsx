import { useEffect, useRef, useState } from "react";
import { renderGeometry } from "../d3/renderGeometry.js";

export default function GeometryCanvas({ geometry }) {
  const svgRef = useRef(null);
  const containerRef = useRef(null);
  const [tooltip, setTooltip] = useState(null);

  useEffect(() => {
    const container = containerRef.current;

    const toLocalPoint = (event) => {
      const rect = container.getBoundingClientRect();
      return { x: event.clientX - rect.left, y: event.clientY - rect.top };
    };

    renderGeometry(svgRef.current, geometry, {
      onNodeEnter: (node, event) => {
        const { x, y } = toLocalPoint(event);
        setTooltip({ x, y, index: node.index, entropy: node.entropy });
      },
      onNodeMove: (node, event) => {
        const { x, y } = toLocalPoint(event);
        setTooltip({ x, y, index: node.index, entropy: node.entropy });
      },
      onNodeLeave: () => setTooltip(null),
    });
  }, [geometry]);

  return (
    <div className="geometry-canvas" ref={containerRef}>
      <svg ref={svgRef} role="img" aria-label="Boundary qubits and emergent bulk geometry" />
      {tooltip && (
        <div
          className="geometry-tooltip"
          style={{ left: tooltip.x + 14, top: tooltip.y + 14 }}
        >
          <strong>Qubit {tooltip.index + 1}</strong>
          <span>S = {tooltip.entropy.toFixed(3)} bits</span>
        </div>
      )}
    </div>
  );
}
