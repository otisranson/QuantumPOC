// Mirrors backend/app/path_integral.py — kept in sync manually since this is a small POC.
export const GRID_SIZE = 64;
export const HBAR_MIN = 0.02;
export const HBAR_MAX = 2.5;
export const HBAR_DEFAULT = Math.sqrt(HBAR_MIN * HBAR_MAX);
export const NUM_PATHS_MIN = 20;
export const NUM_PATHS_MAX = 500;
export const NUM_PATHS_DEFAULT = 150;
