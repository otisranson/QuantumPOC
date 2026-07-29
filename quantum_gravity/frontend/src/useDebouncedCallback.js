import { useCallback, useEffect, useRef } from "react";

export function useDebouncedCallback(callback, delayMs) {
  const timeoutRef = useRef(null);

  useEffect(() => () => clearTimeout(timeoutRef.current), []);

  return useCallback(
    (...args) => {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = setTimeout(() => callback(...args), delayMs);
    },
    [callback, delayMs],
  );
}
