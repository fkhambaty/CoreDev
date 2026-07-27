#!/usr/bin/env node
/**
 * CLI: read a trajectory JSON (from a file argument or stdin) and print a
 * scored report as JSON.
 *
 *   npm run score -- path/to/trajectory.json
 *   cat trajectory.json | npm run score
 */

import { readFileSync } from "node:fs";
import { scoreTrajectory, type Trajectory } from "./scorer.js";

function readInput(): string {
  const fileArg = process.argv[2];
  if (fileArg) {
    return readFileSync(fileArg, "utf-8");
  }
  return readFileSync(0, "utf-8"); // fd 0 = stdin
}

function main(): void {
  const raw = readInput().trim();
  if (!raw) {
    console.error("No trajectory JSON provided (pass a file path or pipe via stdin).");
    process.exit(2);
  }

  let trajectory: Trajectory;
  try {
    trajectory = JSON.parse(raw) as Trajectory;
  } catch (error) {
    console.error(`Invalid JSON: ${(error as Error).message}`);
    process.exit(2);
    return;
  }

  const report = scoreTrajectory(trajectory);
  console.log(JSON.stringify(report, null, 2));
  process.exit(report.verdict === "fail" ? 1 : 0);
}

main();
