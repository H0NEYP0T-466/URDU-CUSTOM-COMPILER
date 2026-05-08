import type { TACInfo } from "../types/compiler";
import "./TACPanel.css";

interface TACPanelProps {
  data: TACInfo | null;
}

/** Classify a TAC line for syntax coloring */
function getLineClass(line: string): string {
  const trimmed = line.trim();
  if (trimmed.endsWith(":")) return "tac-panel__line--label";
  if (trimmed.startsWith("goto ") || trimmed.startsWith("iffalse "))
    return "tac-panel__line--control";
  if (trimmed.startsWith("print ")) return "tac-panel__line--print";
  return "";
}

/** Check if a line was changed during optimization */
function isChanged(original: string[], optimized: string[], line: string): boolean {
  const inOrig = original.includes(line);
  const inOpt = optimized.includes(line);
  // It's a new/modified line if it's in optimized but not original
  return !inOrig && inOpt;
}

export default function TACPanel({ data }: TACPanelProps) {
  if (!data) {
    return (
      <div className="tac-panel">
        <div className="tac-panel__empty">
          <div>⚡</div>
          <div>Code chalao to TAC dikhega</div>
        </div>
      </div>
    );
  }

  return (
    <div className="tac-panel" id="tac-panel">
      {/* Side-by-side columns */}
      <div className="tac-panel__columns">
        {/* Original TAC */}
        <div className="tac-panel__column">
          <div className="tac-panel__column-header tac-panel__column-header--original">
            📄 Before Optimization ({data.original.length} instructions)
          </div>
          <div className="tac-panel__code">
            {data.original.map((line, i) => (
              <div
                key={i}
                className={`tac-panel__line ${getLineClass(line)}`}
              >
                <span className="tac-panel__line-num">{i}</span>
                <span className="tac-panel__line-content">{line}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Optimized TAC */}
        <div className="tac-panel__column">
          <div className="tac-panel__column-header tac-panel__column-header--optimized">
            ✨ After Optimization ({data.optimized.length} instructions)
          </div>
          <div className="tac-panel__code">
            {data.optimized.map((line, i) => {
              const changed = isChanged(data.original, data.optimized, line);
              return (
                <div
                  key={i}
                  className={`tac-panel__line ${getLineClass(line)} ${
                    changed ? "tac-panel__line--changed" : ""
                  }`}
                >
                  <span className="tac-panel__line-num">{i}</span>
                  <span className="tac-panel__line-content">{line}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Changes log */}
      <div className="tac-panel__changes">
        <div className="tac-panel__changes-title">
          🔧 Optimization Changes ({data.changes.length})
        </div>
        {data.changes.map((change, i) => (
          <div key={i} className="tac-panel__change-item">
            {change}
          </div>
        ))}
      </div>
    </div>
  );
}
