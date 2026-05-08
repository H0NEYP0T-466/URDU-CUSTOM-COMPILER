/** All TypeScript interfaces for the compiler API responses */

export interface TokenInfo {
  index: number;
  type: string;
  value: string;
  line: number;
}

export interface SymbolEntryInfo {
  name: string;
  var_type: string;
  scope: string;
  scope_depth: number;
}

export interface SemanticInfo {
  errors: string[];
  warnings: string[];
  symbol_table: Record<string, string>;
  scoped_symbols: SymbolEntryInfo[];
}

export interface TACInfo {
  original: string[];
  optimized: string[];
  changes: string[];
}

export interface ErrorMarker {
  line: number;
  message: string;
  severity: "error" | "warning";
}

export interface CompilerResponse {
  output: string;
  error: string | null;
  error_line: number | null;
  error_markers: ErrorMarker[];
  tokens: TokenInfo[];
  ast: string;
  semantic: SemanticInfo | null;
  tac: TACInfo | null;
  generated_python: string;
}
