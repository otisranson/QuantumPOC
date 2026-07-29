import { Canvas } from "@react-three/fiber";
import FieldMesh from "./FieldMesh.jsx";
import DragHandle from "./DragHandle.jsx";
import { domainToScreenPct, screenPctToDomain } from "../utils/domain.js";

export default function FieldCanvas({ field, start, end, onStartChange, onEndChange }) {
  const [startPctX, startPctY] = domainToScreenPct(start[0], start[1]);
  const [endPctX, endPctY] = domainToScreenPct(end[0], end[1]);

  return (
    <div className="field-canvas">
      <Canvas frameloop="demand">
        <FieldMesh field={field} />
      </Canvas>
      <DragHandle
        pctX={startPctX}
        pctY={startPctY}
        color="#22d3ee"
        label="Start point"
        onChange={(pctX, pctY) => onStartChange(screenPctToDomain(pctX, pctY))}
      />
      <DragHandle
        pctX={endPctX}
        pctY={endPctY}
        color="#ffffff"
        label="End point"
        onChange={(pctX, pctY) => onEndChange(screenPctToDomain(pctX, pctY))}
      />
    </div>
  );
}
