import { HBAR_MAX, HBAR_MIN, NUM_PATHS_MAX, NUM_PATHS_MIN } from "../constants.js";

// hbar's visible effect is multiplicative (S/hbar), so the slider must be
// linear in log10(hbar), not in hbar itself -- otherwise nearly all of the
// slider's travel sits in the already-fully-classical region.
const LOG_MIN = Math.log10(HBAR_MIN);
const LOG_MAX = Math.log10(HBAR_MAX);
const hbarToPos = (hbar) => (Math.log10(hbar) - LOG_MIN) / (LOG_MAX - LOG_MIN);
const posToHbar = (pos) => 10 ** (LOG_MIN + pos * (LOG_MAX - LOG_MIN));

export default function ControlPanel({ hbar, onHbarChange, numPaths, onNumPathsChange, mode, onModeChange }) {
  return (
    <div className="control-panel">
      <div className="control-row">
        <label htmlFor="hbar-slider">quantum &harr; classical (&#295;)</label>
        <input
          id="hbar-slider"
          type="range"
          min="0"
          max="1"
          step="0.001"
          value={hbarToPos(hbar)}
          onChange={(event) => onHbarChange(posToHbar(Number(event.target.value)))}
        />
        <span className="control-value">{hbar.toFixed(3)}</span>
      </div>

      <div className="control-row">
        <label htmlFor="paths-slider">paths</label>
        <input
          id="paths-slider"
          type="range"
          min={NUM_PATHS_MIN}
          max={NUM_PATHS_MAX}
          step="1"
          value={numPaths}
          disabled={mode !== "computed"}
          onChange={(event) => onNumPathsChange(Number(event.target.value))}
        />
        <span className="control-value">{numPaths}</span>
      </div>

      <div className="mode-toggle" role="radiogroup" aria-label="Field source">
        <button
          type="button"
          role="radio"
          aria-checked={mode === "computed"}
          className={mode === "computed" ? "active" : ""}
          onClick={() => onModeChange("computed")}
        >
          computed
        </button>
        <button
          type="button"
          role="radio"
          aria-checked={mode === "learned"}
          className={mode === "learned" ? "active" : ""}
          onClick={() => onModeChange("learned")}
        >
          learned
        </button>
      </div>
    </div>
  );
}
