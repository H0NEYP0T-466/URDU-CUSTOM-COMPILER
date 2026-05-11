/** API client for the Urdu compiler backend */

import type { CompilerResponse } from "../types/compiler";

const API_BASE = "http://localhost:8008";

export async function runCode(code: string): Promise<CompilerResponse> {
  const response = await fetch(`${API_BASE}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });

  if (!response.ok) {
    throw new Error(`Server error: ${response.status}`);
  }

  return response.json();
}
