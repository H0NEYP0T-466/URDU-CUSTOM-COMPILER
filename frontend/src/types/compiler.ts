/** All TypeScript interfaces for the compiler API responses */

export interface TokenInfo {
  index: number;
  type: string;
  value: string;
  line: number;
}

export interface SemanticInfo {
  errors: string[];
  warnings: string[];
  symbol_table: Record<string, string>;
}

export interface TACInfo {
  original: string[];
  optimized: string[];
  changes: string[];
}

export interface CompilerResponse {
  output: string;
  error: string | null;
  tokens: TokenInfo[];
  ast: string;
  semantic: SemanticInfo | null;
  tac: TACInfo | null;
  generated_python: string;
}
