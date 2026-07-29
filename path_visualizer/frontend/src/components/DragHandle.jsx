import { useCallback, useRef } from "react";

const clampPct = (v) => Math.min(100, Math.max(0, v));

export default function DragHandle({ pctX, pctY, onChange, label, color }) {
  const draggingRef = useRef(false);

  const updateFromEvent = useCallback(
    (event) => {
      const container = event.currentTarget.parentElement;
      const rect = container.getBoundingClientRect();
      const x = clampPct(((event.clientX - rect.left) / rect.width) * 100);
      const y = clampPct(((event.clientY - rect.top) / rect.height) * 100);
      onChange(x, y);
    },
    [onChange],
  );

  const handlePointerDown = (event) => {
    event.currentTarget.setPointerCapture(event.pointerId);
    draggingRef.current = true;
    updateFromEvent(event);
  };

  const handlePointerMove = (event) => {
    if (!draggingRef.current) return;
    updateFromEvent(event);
  };

  const handlePointerUp = (event) => {
    draggingRef.current = false;
    event.currentTarget.releasePointerCapture(event.pointerId);
  };

  return (
    <div
      className="drag-handle"
      style={{ left: `${pctX}%`, top: `${pctY}%`, borderColor: color }}
      onPointerDown={handlePointerDown}
      onPointerMove={handlePointerMove}
      onPointerUp={handlePointerUp}
      role="slider"
      aria-label={label}
      aria-valuetext={label}
      tabIndex={0}
    >
      <span className="drag-handle-label">{label}</span>
    </div>
  );
}
