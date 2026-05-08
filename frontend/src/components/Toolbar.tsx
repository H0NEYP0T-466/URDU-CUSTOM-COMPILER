import "./Toolbar.css";

interface ToolbarProps {
  onRun: () => void;
  onClear: () => void;
  onToggleSidebar: () => void;
  isRunning: boolean;
}

export default function Toolbar({ onRun, onClear, onToggleSidebar, isRunning }: ToolbarProps) {
  return (
    <header className="toolbar" id="toolbar">
      <div className="toolbar__title-group">
        <button
          className="toolbar__toggle-sidebar"
          onClick={onToggleSidebar}
          title="Toggle Examples"
          id="toggle-sidebar-btn"
        >
          ☰
        </button>
        <h1 className="toolbar__title">URDU-CUSTOM-COMPILER</h1>
        <span className="toolbar__subtitle">ایک کسٹم زبان</span>
      </div>

      <div className="toolbar__actions">
        <button
          className="toolbar__btn toolbar__btn--run"
          onClick={onRun}
          disabled={isRunning}
          id="run-btn"
        >
          {isRunning ? (
            <>
              <span className="toolbar__spinner" />
              Chal raha hai…
            </>
          ) : (
            <>Chalao ▶</>
          )}
        </button>
        <button
          className="toolbar__btn toolbar__btn--clear"
          onClick={onClear}
          id="clear-btn"
        >
          Saaf Karo ✕
        </button>
      </div>
    </header>
  );
}
