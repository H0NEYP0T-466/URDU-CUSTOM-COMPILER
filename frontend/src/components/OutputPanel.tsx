import { useState } from "react";
import type { CompilerResponse } from "../types/compiler";
import SemanticPanel from "./SemanticPanel";
import TACPanel from "./TACPanel";
import PythonPanel from "./PythonPanel";
import "./OutputPanel.css";

type TabId = "output" | "tokens" | "ast" | "semantic" | "tac" | "python";

interface Tab {
  id: TabId;
  label: string;
  icon: string;
}

const TABS: Tab[] = [
  { id: "output", label: "Output", icon: "▶" },
  { id: "tokens", label: "Tokens", icon: "🔤" },
  { id: "ast", label: "AST", icon: "🌳" },
  { id: "semantic", label: "Semantic", icon: "🔍" },
  { id: "tac", label: "TAC", icon: "⚡" },
  { id: "python", label: "Python", icon: "🐍" },
];

interface OutputPanelProps {
  data: CompilerResponse | null;
  error: string | null;
  executionTime: number | null;
}

export default function OutputPanel({
  data,
  error,
  executionTime,
}: OutputPanelProps) {
  const [activeTab, setActiveTab] = useState<TabId>("output");

  const output = data?.output ?? "";
  const lines = output ? output.split("\n") : [];
  const displayError = error || data?.error || null;
  const hasContent = lines.length > 0 || displayError;

  const dotClass = displayError
    ? "output-panel__title-dot--error"
    : hasContent
    ? "output-panel__title-dot--success"
    : "output-panel__title-dot--idle";

  /** Render badge for a tab */
  const renderBadge = (tabId: TabId) => {
    if (tabId === "tokens" && data?.tokens?.length) {
      return (
        <span className="output-panel__tab-badge output-panel__tab-badge--count">
          {data.tokens.length}
        </span>
      );
    }
    if (tabId === "semantic" && data?.semantic) {
      if (data.semantic.errors.length > 0) {
        return (
          <span className="output-panel__tab-badge output-panel__tab-badge--error">
            {data.semantic.errors.length}
          </span>
        );
      }
      if (data.semantic.warnings.length > 0) {
        return (
          <span className="output-panel__tab-badge output-panel__tab-badge--warning">
            {data.semantic.warnings.length}
          </span>
        );
      }
    }
    return null;
  };

  return (
    <div className="output-panel" id="output-panel">
      {/* ── Tab bar ── */}
      <div className="output-panel__tabs">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            className={`output-panel__tab ${
              activeTab === tab.id ? "output-panel__tab--active" : ""
            }`}
            onClick={() => setActiveTab(tab.id)}
            id={`tab-${tab.id}`}
          >
            {tab.icon} {tab.label}
            {renderBadge(tab.id)}
          </button>
        ))}
      </div>

      {/* ── Tab content ── */}
      <div className="output-panel__content">
        {/* Output Terminal */}
        {activeTab === "output" && (
          <div className="output-panel__terminal">
            <div className="output-panel__terminal-header">
              <div className="output-panel__title">
                <span className={`output-panel__title-dot ${dotClass}`} />
                Output Terminal
              </div>
              {executionTime !== null && (
                <span className="output-panel__time">
                  ⏱ {executionTime.toFixed(0)}ms
                </span>
              )}
            </div>

            {!hasContent ? (
              <div className="output-panel__empty">
                <div className="output-panel__empty-icon">⟩_</div>
                <div className="output-panel__empty-text">
                  Koi output nahi hai
                </div>
                <div className="output-panel__empty-hint">
                  Code likho aur &quot;Chalao ▶&quot; dabao
                </div>
              </div>
            ) : (
              <>
                {lines.map((line, index) => (
                  <div
                    key={index}
                    className="output-panel__line output-panel__line--animate"
                    style={{ animationDelay: `${index * 30}ms` }}
                  >
                    {line}
                  </div>
                ))}
                {displayError && (
                  <div className="output-panel__error">❌ {displayError}</div>
                )}
              </>
            )}
          </div>
        )}

        {/* Tokens Table */}
        {activeTab === "tokens" && (
          <div className="output-panel__tokens">
            {data?.tokens?.length ? (
              <table className="output-panel__tokens-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Type</th>
                    <th>Value</th>
                    <th>Line</th>
                  </tr>
                </thead>
                <tbody>
                  {data.tokens.map((tok) => (
                    <tr key={tok.index}>
                      <td>{tok.index}</td>
                      <td>
                        <span
                          className={`output-panel__token-type--${tok.type}`}
                        >
                          {tok.type}
                        </span>
                      </td>
                      <td>{tok.value}</td>
                      <td>{tok.line}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="output-panel__empty">
                <div>🔤</div>
                <div className="output-panel__empty-text">
                  Code chalao to tokens dikhenge
                </div>
              </div>
            )}
          </div>
        )}

        {/* AST Tree */}
        {activeTab === "ast" && (
          <div className="output-panel__ast">
            {data?.ast ? (
              data.ast
            ) : (
              <div className="output-panel__empty">
                <div>🌳</div>
                <div className="output-panel__empty-text">
                  Code chalao to AST dikhega
                </div>
              </div>
            )}
          </div>
        )}

        {/* Semantic Analysis */}
        {activeTab === "semantic" && (
          <SemanticPanel data={data?.semantic ?? null} />
        )}

        {/* TAC */}
        {activeTab === "tac" && <TACPanel data={data?.tac ?? null} />}

        {/* Python Code */}
        {activeTab === "python" && (
          <PythonPanel code={data?.generated_python ?? ""} />
        )}
      </div>

      {/* Footer */}
      {executionTime !== null && activeTab === "output" && (
        <div className="output-panel__footer">
          <span className="output-panel__time">
            Execution: {executionTime.toFixed(0)}ms
          </span>
        </div>
      )}
    </div>
  );
}
