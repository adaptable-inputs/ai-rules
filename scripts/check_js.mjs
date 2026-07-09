#!/usr/bin/env node
/**
 * Syntax-only parse of ts/tsx/js/jsx fenced blocks.
 *
 * Reads a JSON array of {file, line, tag, code} on stdin, prints one error
 * line per block that fails to PARSE. Type errors are deliberately ignored:
 * paired Do/Don't snippets reference types they never declare.
 *
 * Exit 1 if any block failed to parse, 0 otherwise.
 */
import ts from "typescript";

const stdin = await new Promise((resolve) => {
  let buf = "";
  process.stdin.setEncoding("utf8");
  process.stdin.on("data", (d) => (buf += d));
  process.stdin.on("end", () => resolve(buf));
});

const jobs = JSON.parse(stdin || "[]");
const KIND = { ts: ts.ScriptKind.TS, tsx: ts.ScriptKind.TSX, js: ts.ScriptKind.JS, jsx: ts.ScriptKind.JSX };

let failed = 0;
for (const { file, line, tag, code } of jobs) {
  const sf = ts.createSourceFile(`snippet.${tag}`, code, ts.ScriptTarget.Latest,
                                 /*setParentNodes*/ false, KIND[tag]);
  // parseDiagnostics is internal but stable; it holds syntax errors only.
  const diags = sf.parseDiagnostics;
  if (!Array.isArray(diags)) {
    // Fail loud rather than silently verifying nothing.
    console.error(`parseDiagnostics unavailable on this typescript build`);
    process.exit(2);
  }
  for (const d of diags) {
    const msg = ts.flattenDiagnosticMessageText(d.messageText, " ");
    const { line: dl } = sf.getLineAndCharacterOfPosition(d.start ?? 0);
    console.log(`${file}:${line}: ${tag} block does not parse at snippet line ${dl + 1}: ${msg}`);
    failed++;
  }
}
// Sentinel: proves the parser ran to completion. The caller requires it.
console.log(`OK ${jobs.length}`);
process.exit(failed ? 1 : 0);
