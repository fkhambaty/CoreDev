# agent-lab-scorer (TypeScript)

A tiny, dependency-light TypeScript CLI that scores agent **trajectories**
against the same rubric logic as the Python core. It reads the exact JSON that
`agent_lab.Trajectory.to_json()` produces, so both languages evaluate the same
artifact and agree on the verdict — a small demonstration of cross-language
parity.

## Install & run

```bash
cd ts
npm install
npm test          # vitest
npm run typecheck # tsc --noEmit

# score a trajectory produced by the Python agent:
python3 -c "import sys; sys.path.insert(0,'../src'); from agent_lab import ToolCallingAgent; print(ToolCallingAgent().run('12 + 30').to_json())" \
  | npm run score
```

## Layout

```
src/scorer.ts   # trajectory scoring + verdict logic (union-exhaustive)
src/cli.ts      # reads JSON from a file arg or stdin, prints a report
test/           # vitest suite
```
