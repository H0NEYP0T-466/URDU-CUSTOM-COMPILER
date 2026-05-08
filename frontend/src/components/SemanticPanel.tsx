import type { SemanticInfo } from "../types/compiler";
import "./SemanticPanel.css";

interface SemanticPanelProps {
  data: SemanticInfo | null;
}

export default function SemanticPanel({ data }: SemanticPanelProps) {
  if (!data) {
    return (
      <div className="semantic-panel">
        <div className="semantic-panel__empty">
          <div>🔍</div>
          <div>Code chalao to semantic analysis dikhega</div>
        </div>
      </div>
    );
  }

  const hasSymbols = Object.keys(data.symbol_table).length > 0;
  const noIssues = data.errors.length === 0 && data.warnings.length === 0;

  return (
    <div className="semantic-panel" id="semantic-panel">
      {/* Success banner when no errors */}
      {data.errors.length === 0 && (
        <div className="semantic-panel__success">
          <span className="semantic-panel__success-icon">✅</span>
          Semantic check passed — koi error nahi
        </div>
      )}

      {/* Symbol Table */}
      {hasSymbols && (
        <div>
          <div className="semantic-panel__section-title">
            📋 Symbol Table
          </div>
          <table className="semantic-panel__table">
            <thead>
              <tr>
                <th>Variable</th>
                <th>Type</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(data.symbol_table).map(([name, type]) => (
                <tr key={name}>
                  <td>
                    <span className="semantic-panel__var-name">{name}</span>
                  </td>
                  <td>
                    <span className="semantic-panel__var-type">{type}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Warnings */}
      {data.warnings.length > 0 && (
        <div>
          <div className="semantic-panel__section-title">
            ⚠️ Warnings ({data.warnings.length})
          </div>
          {data.warnings.map((warning, i) => (
            <div key={i} className="semantic-panel__warning">
              <span className="semantic-panel__warning-icon">⚠</span>
              {warning}
            </div>
          ))}
        </div>
      )}

      {/* Errors */}
      {data.errors.length > 0 && (
        <div>
          <div className="semantic-panel__section-title">
            ❌ Errors ({data.errors.length})
          </div>
          {data.errors.map((error, i) => (
            <div key={i} className="semantic-panel__error">
              <span className="semantic-panel__error-icon">✗</span>
              {error}
            </div>
          ))}
        </div>
      )}

      {/* If truly empty */}
      {!hasSymbols && noIssues && (
        <div className="semantic-panel__empty">
          <div>Koi variable ya issue nahi mila</div>
        </div>
      )}
    </div>
  );
}
