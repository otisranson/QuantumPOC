function qubitLabel(gate) {
  if (!gate) return '';
  if (gate.qubits.length === 2) return 'q0, q1';
  return `q${gate.qubits[0]}`;
}

export default function GateCard({ gate }) {
  if (!gate) {
    return (
      <div className="flex h-full min-h-[9rem] flex-col items-center justify-center rounded-sm border border-dashed border-ink/25 bg-paper-dark/40 px-6 py-5 text-center">
        <p className="font-mono text-xs uppercase tracking-[0.2em] text-ink-soft/70">
          Awaiting input
        </p>
        <p className="mt-2 font-display text-sm italic text-ink-soft/60">
          Press a key to reveal its gate
        </p>
      </div>
    );
  }

  return (
    <div className="flex h-full min-h-[9rem] flex-col justify-between rounded-sm border border-ink/15 bg-paper-dark/50 px-6 py-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-brass">Now playing</p>
          <h3 className="mt-1 font-display text-3xl font-semibold text-ink">{gate.fullName}</h3>
        </div>
        <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-sm border-2 border-ink bg-paper font-mono text-lg font-semibold text-ink">
          {gate.symbol}
        </div>
      </div>
      <p className="mt-3 font-display text-base leading-snug text-ink-soft">{gate.description}</p>
      <div className="mt-4 flex items-center gap-2 font-mono text-xs uppercase tracking-[0.15em] text-verdigris">
        <span className="inline-block h-1.5 w-1.5 rounded-full bg-verdigris" />
        target {qubitLabel(gate)}
      </div>
    </div>
  );
}
