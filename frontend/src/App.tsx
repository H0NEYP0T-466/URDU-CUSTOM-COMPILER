import { useState, useCallback, useRef, useEffect } from "react";
import type { CompilerResponse } from "./types/compiler";
import Toolbar from "./components/Toolbar";
import ExamplesPanel from "./components/ExamplesPanel";
import Editor from "./components/Editor";
import OutputPanel from "./components/OutputPanel";
import { runCode } from "./api/compiler";
import "./App.css";

const DEFAULT_CODE = `# Assalam o Alaikum! Yeh URDU-CUSTOM-COMPILER hai
# Neeche apna code likho ya kisi misaal pe click karo

rakho naam = "Duniya"
dikhao "Assalam o Alaikum, "
dikhao naam
`;

/** Min width percentage for either panel */
const MIN_PANEL_PCT = 20;
const MAX_PANEL_PCT = 80;

export default function App() {
  const [code, setCode] = useState(DEFAULT_CODE);
  const [compilerData, setCompilerData] = useState<CompilerResponse | null>(
    null
  );
  const [connectionError, setConnectionError] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [executionTime, setExecutionTime] = useState<number | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // ── Resizable split ──
  const [editorPct, setEditorPct] = useState(60); // editor width as % of main area
  const isDragging = useRef(false);
  const mainRef = useRef<HTMLDivElement>(null);

  const handleMouseDown = useCallback(() => {
    isDragging.current = true;
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";
  }, []);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging.current || !mainRef.current) return;
      const rect = mainRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      let pct = (x / rect.width) * 100;
      pct = Math.max(MIN_PANEL_PCT, Math.min(MAX_PANEL_PCT, pct));
      setEditorPct(pct);
    };

    const handleMouseUp = () => {
      if (isDragging.current) {
        isDragging.current = false;
        document.body.style.cursor = "";
        document.body.style.userSelect = "";
      }
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, []);

  const handleRun = useCallback(async () => {
    setIsRunning(true);
    setCompilerData(null);
    setConnectionError(null);
    setExecutionTime(null);

    const startTime = performance.now();

    try {
      const result = await runCode(code);
      const elapsed = performance.now() - startTime;
      setExecutionTime(elapsed);
      setCompilerData(result);
    } catch (err) {
      const elapsed = performance.now() - startTime;
      setExecutionTime(elapsed);
      setConnectionError(
        err instanceof Error
          ? `Connection Error: ${err.message}`
          : "Unknown error occurred"
      );
    } finally {
      setIsRunning(false);
    }
  }, [code]);

  const handleClear = useCallback(() => {
    setCompilerData(null);
    setConnectionError(null);
    setExecutionTime(null);
  }, []);

  const handleSelectExample = useCallback((exampleCode: string) => {
    setCode(exampleCode);
    setCompilerData(null);
    setConnectionError(null);
    setExecutionTime(null);
  }, []);

  const handleToggleSidebar = useCallback(() => {
    setSidebarOpen((prev) => !prev);
  }, []);

  return (
    <div className="app" id="app">
      <Toolbar
        onRun={handleRun}
        onClear={handleClear}
        onToggleSidebar={handleToggleSidebar}
        isRunning={isRunning}
      />
      <div className="app__workspace">
        <ExamplesPanel
          isOpen={sidebarOpen}
          onSelectExample={handleSelectExample}
        />
        <div className="app__main" ref={mainRef}>
          <div
            className="app__editor-wrapper"
            style={{ flexBasis: `${editorPct}%`, flexGrow: 0, flexShrink: 0 }}
          >
            <Editor
              code={code}
              onChange={setCode}
              errorMarkers={compilerData?.error_markers ?? []}
            />
          </div>
          <div
            className="app__resize-handle"
            onMouseDown={handleMouseDown}
          />
          <div
            className="app__output-wrapper"
            style={{ flexBasis: `${100 - editorPct}%`, flexGrow: 0, flexShrink: 0 }}
          >
            <OutputPanel
              data={compilerData}
              error={connectionError}
              executionTime={executionTime}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
