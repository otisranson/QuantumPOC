import { useCallback, useMemo, useState } from 'react';

let instanceCounter = 0;
function nextInstanceId() {
  instanceCounter += 1;
  return `gate-${instanceCounter}`;
}

export const MODES = {
  FREEPLAY: 'freeplay',
  RECORDING: 'recording',
  LOCKED: 'locked',
};

// Owns the mode state machine (freeplay / recording / locked), the
// accumulated circuit, and the "last played" gate shown by the gate card.
export function useQuantumCircuit() {
  const [mode, setMode] = useState(MODES.FREEPLAY);
  const [circuit, setCircuit] = useState([]);
  const [activeGate, setActiveGate] = useState(null);

  const playGate = useCallback(
    (gateDef) => {
      setActiveGate(gateDef);
      setMode((currentMode) => {
        if (currentMode === MODES.RECORDING) {
          setCircuit((prev) => [...prev, { ...gateDef, instanceId: nextInstanceId() }]);
        }
        return currentMode;
      });
    },
    [],
  );

  const startRecording = useCallback(() => {
    setCircuit([]);
    setActiveGate(null);
    setMode(MODES.RECORDING);
  }, []);

  const endRecording = useCallback(() => {
    setMode((currentMode) => (currentMode === MODES.RECORDING ? MODES.LOCKED : currentMode));
  }, []);

  const clearCircuit = useCallback(() => {
    setCircuit([]);
    setActiveGate(null);
  }, []);

  const resetAll = useCallback(() => {
    setMode(MODES.FREEPLAY);
    setCircuit([]);
    setActiveGate(null);
  }, []);

  const displayedGates = useMemo(() => {
    if (mode === MODES.FREEPLAY) {
      return activeGate ? [{ ...activeGate, instanceId: 'freeplay-gate' }] : [];
    }
    return circuit;
  }, [mode, activeGate, circuit]);

  return {
    mode,
    circuit,
    activeGate,
    displayedGates,
    playGate,
    startRecording,
    endRecording,
    clearCircuit,
    resetAll,
  };
}
