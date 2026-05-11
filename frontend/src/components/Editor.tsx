import { useRef, useCallback, useEffect } from "react";
import MonacoEditor, { type OnMount } from "@monaco-editor/react";
import type { editor } from "monaco-editor";
import type { ErrorMarker } from "../types/compiler";
import "./Editor.css";

interface EditorProps {
  code: string;
  onChange: (value: string) => void;
  errorMarkers?: ErrorMarker[];
}

/** Urdu language keywords for custom highlighting */
const URDU_KEYWORDS = [
  "rakho", "dikhao", "agar", "warna",
  "jabtak", "khatam", "sahi", "ghalat",
  "aur", "ya",
  "banao", "wapis", "karo",
  "input", "int", "str",
];

export default function Editor({ code, onChange, errorMarkers = [] }: EditorProps) {
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);
  const monacoRef = useRef<typeof import("monaco-editor") | null>(null);

  const handleMount: OnMount = useCallback((editorInstance, monaco) => {
    editorRef.current = editorInstance;
    monacoRef.current = monaco;

    // Register custom language
    monaco.languages.register({ id: "urdu-lang" });

    // Tokenizer for syntax highlighting
    monaco.languages.setMonarchTokensProvider("urdu-lang", {
      keywords: URDU_KEYWORDS,
      tokenizer: {
        root: [
          // Strings
          [/"[^"]*"/, "string"],
          // Comments
          [/#.*$/, "comment"],
          // Numbers
          [/\b\d+(\.\d+)?\b/, "number"],
          // Keywords
          [
            /\b(rakho|dikhao|agar|warna|jabtak|khatam|sahi|ghalat|aur|ya|banao|wapis|karo|input|int|str)\b/,
            "keyword",
          ],
          // Operators
          [/[>=<!]=?|[+\-*/]/, "operator"],
          // Identifiers
          [/[a-zA-Z_]\w*/, "identifier"],
        ],
      },
    });

    // Define custom theme
    monaco.editor.defineTheme("urdu-dark", {
      base: "vs-dark",
      inherit: true,
      rules: [
        { token: "keyword", foreground: "14d4c4", fontStyle: "bold" },
        { token: "string", foreground: "ce9178" },
        { token: "number", foreground: "b5cea8" },
        { token: "comment", foreground: "6a9955", fontStyle: "italic" },
        { token: "operator", foreground: "d4d4d4" },
        { token: "identifier", foreground: "9cdcfe" },
      ],
      colors: {
        "editor.background": "#1a1a2e",
        "editor.foreground": "#e2e8f0",
        "editor.lineHighlightBackground": "#1f2940",
        "editor.selectionBackground": "#264f78",
        "editorCursor.foreground": "#14d4c4",
        "editorLineNumber.foreground": "#4a5568",
        "editorLineNumber.activeForeground": "#14d4c4",
      },
    });

    // Apply the custom theme
    monaco.editor.setTheme("urdu-dark");

    // Focus the editor
    editorInstance.focus();
  }, []);

  // -- Error markers: update whenever errorMarkers change --
  useEffect(() => {
    const editorInstance = editorRef.current;
    const monaco = monacoRef.current;
    if (!editorInstance || !monaco) return;

    const model = editorInstance.getModel();
    if (!model) return;

    if (errorMarkers.length === 0) {
      // Clear all markers
      monaco.editor.setModelMarkers(model, "urdu-compiler", []);
      return;
    }

    const markers: editor.IMarkerData[] = errorMarkers.map((marker) => {
      const lineNumber = Math.max(1, Math.min(marker.line, model.getLineCount()));
      const lineContent = model.getLineContent(lineNumber);
      return {
        severity:
          marker.severity === "error"
            ? monaco.MarkerSeverity.Error
            : monaco.MarkerSeverity.Warning,
        message: marker.message,
        startLineNumber: lineNumber,
        startColumn: 1,
        endLineNumber: lineNumber,
        endColumn: lineContent.length + 1,
      };
    });

    monaco.editor.setModelMarkers(model, "urdu-compiler", markers);
  }, [errorMarkers]);

  const handleChange = useCallback(
    (value: string | undefined) => {
      onChange(value ?? "");
    },
    [onChange]
  );

  const lineCount = code.split("\n").length;

  return (
    <div className="editor" id="editor-panel">
      <div className="editor__header">
        <div className="editor__tab">
          <span className="editor__tab-dot" />
          main.urdu
        </div>
        <span className="editor__line-count">{lineCount} lines</span>
      </div>
      <div className="editor__monaco">
        <MonacoEditor
          height="100%"
          language="urdu-lang"
          theme="urdu-dark"
          value={code}
          onChange={handleChange}
          onMount={handleMount}
          options={{
            fontSize: 15,
            fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
            fontLigatures: true,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            lineNumbers: "on",
            renderLineHighlight: "line",
            padding: { top: 12 },
            smoothScrolling: true,
            cursorBlinking: "smooth",
            cursorSmoothCaretAnimation: "on",
            bracketPairColorization: { enabled: true },
            wordWrap: "on",
            tabSize: 4,
            automaticLayout: true,
            glyphMargin: true,
          }}
        />
      </div>
    </div>
  );
}
