/**
 * App.tsx — the whole interface. It holds no audio logic at all; that is live.ts,
 * exactly as `app.py` holds no model logic in the other projects.
 */

import { useCallback, useEffect, useRef, useState } from "react";
import { Call, type CallState, type Line } from "./live";
import "./styles.css";

const PROMPTS = [
  "What is the interest rate on a home loan?",
  "What would my monthly payment be on a 50 lakh home loan at 8.4% over 25 years?",
  "And for a car loan instead?",
  "Do you offer loans against gold?",
];

export default function App() {
  const [state, setState] = useState<CallState>("idle");
  const [detail, setDetail] = useState<string>();
  const [lines, setLines] = useState<Line[]>([]);
  const [level, setLevel] = useState(0);
  const call = useRef<Call>(null);
  const transcript = useRef<HTMLDivElement>(null);
  const newBubble = useRef(true); // set when a turn ends, so the next fragment starts a fresh bubble

  // Gemini sends the transcript in fragments; grow the last bubble instead of adding one per fragment.
  const addLine = useCallback((line: Line) => {
    setLines((old) => {
      const last = old[old.length - 1];
      if (last && last.role === line.role && !newBubble.current) {
        return [...old.slice(0, -1), { role: last.role, text: last.text + line.text }];
      }
      newBubble.current = false;
      return [...old, line];
    });
  }, []);

  useEffect(() => {
    transcript.current?.scrollTo({ top: transcript.current.scrollHeight, behavior: "smooth" });
  }, [lines]);

  const begin = async () => {
    setLines([]);
    setDetail(undefined);
    const session = new Call({
      onLine: addLine,
      onTurnComplete: () => (newBubble.current = true),
      onLevel: setLevel,
      onState: (next, why) => {
        setState(next);
        if (why) setDetail(why);
      },
    });
    call.current = session;
    try {
      await session.start();
    } catch (error) {
      setState("ended");
      setDetail(error instanceof Error ? error.message : String(error));
    }
  };

  const end = () => {
    call.current?.hangUp();
    call.current = null;
    setLevel(0);
  };

  const live = state === "listening" || state === "speaking";
  const label: Record<CallState, string> = {
    idle: "Not connected",
    connecting: "Connecting…",
    listening: "Listening — just talk",
    speaking: "Speaking — talk over it to interrupt",
    ended: detail ?? "Call ended",
  };

  return (
    <div className="page">
      <header>
        <div className="mark">M</div>
        <div>
          <h1>Meridian Bank</h1>
          <p>Live voice assistant · Gemini native audio</p>
        </div>
        <span className={`pill ${state}`}>{label[state]}</span>
      </header>

      <main>
        <section className="stage">
          <div className={`orb ${state}`} style={{ "--level": Math.min(1, level * 8) } as React.CSSProperties}>
            <span className="ring one" />
            <span className="ring two" />
            <span className="core" />
          </div>

          {live ? (
            <button className="btn end" onClick={end}>
              End call
            </button>
          ) : (
            <button className="btn start" onClick={begin} disabled={state === "connecting"}>
              {state === "connecting" ? "Connecting…" : "Start call"}
            </button>
          )}

          <div className="hints">
            <p>Try saying</p>
            {PROMPTS.map((prompt) => (
              <span key={prompt}>{prompt}</span>
            ))}
          </div>
        </section>

        <section className="transcript" ref={transcript}>
          {lines.length === 0 && (
            <div className="empty">
              <p>The call transcript appears here.</p>
              <p className="small">
                Both sides are shown — but neither is part of the conversation. The model works in sound
                directly; these words are only a courtesy for the screen.
              </p>
            </div>
          )}
          {lines
            .filter((line) => line.text.trim())
            .map((line, index) => (
              <article key={index} className={line.role}>
                <b>{line.role === "you" ? "You" : "Meridian"}</b>
                <p>{line.text}</p>
              </article>
            ))}
        </section>
      </main>
    </div>
  );
}
