// Single source of truth for the screen <-> physics-domain coordinate mapping.
//
// This convention is load-bearing across three independent places that must
// agree or the rendered field and the drag handles will visually disagree
// about where "the same point" is:
//   1. Backend (path_integral.py): field[row][col], row 0 <-> y = -1 (bottom).
//   2. FieldMesh.jsx: sets `texture.flipY = false` explicitly (never relies
//      on three.js's default, which has differed across versions), so
//      texture v=0 samples data row 0 directly, and PlaneGeometry's default
//      UV has v=0 at the plane's bottom edge -- so data row 0 (y=-1) lands
//      at the visual bottom of the rendered square, matching backend row 0.
//   3. This file: CSS `top`/`left` percentages are top-down/left-right, so
//      `pctY` must be flipped to get bottom-up domain y (pctX needs no flip).
export function screenPctToDomain(pctX, pctY) {
  const x = 2 * (pctX / 100) - 1;
  const y = 1 - 2 * (pctY / 100);
  return [x, y];
}

export function domainToScreenPct(x, y) {
  const pctX = ((x + 1) / 2) * 100;
  const pctY = ((1 - y) / 2) * 100;
  return [pctX, pctY];
}
