# Repository Guidelines

> **Autonomous Execution**: Whatever action you can do yourself, please do yourself. This includes starting apps and verification.

## Project Structure & Module Organization
This monorepo manages the Iborain Safety AI sentry grid using `pnpm` workspaces:
- `packages/protocol/`: Shared binary framing, message types, and Zod schemas (`@pixel-bot/protocol`).
- `apps/backend/`: Google Cloud Run Node.js WebSocket broker connecting edge sentries to Gemini Live.
- `apps/playground/pixel-mock/`: Vite browser simulator for camera feeds, audio I/O, and dispatch testing.
- `apps/pi-client/`: Python drivers (`test_hardware.py`, `robot.py`) for Raspberry Pi Zero 2 W edge nodes.
- `apps/playground/*.html`: Financial models, dossiers, and execution evidence reports.

## Build, Test, and Development Commands
Run commands from the repository root:
- `pnpm install`: Install workspace dependencies.
- `pnpm build`: Build all packages (`packages/protocol`, `apps/backend`).
- `pnpm typecheck`: Run TypeScript type verification across all workspaces.
- `pnpm run dev:backend`: Launch backend broker in watch mode (`MODE=echo` or `MODE=gemini`).
- `pnpm run dev:mock`: Launch Vite playground client for browser-based testing.
- `SOAK_MINUTES=2 pnpm run soak`: Execute automated end-to-end WebSocket soak and resilience tests.

## Coding Style & Naming Conventions
- **TypeScript**: 2-space indentation, ES modules (`"type": "module"`), strict mode via `tsconfig.base.json`.
- **Python**: PEP 8 standards, 4-space indentation.
- **Naming**: `kebab-case` for file/directory names; `PascalCase` for types, classes, and interfaces; `camelCase` for functions/variables.
- **Protocol Schemas**: Define and validate all wire payloads using Zod in `packages/protocol/src/index.ts`.

## Testing Guidelines
- **Type Integrity**: Run `pnpm typecheck` before submitting changes.
- **Soak & Stress Testing**: Run `pnpm run soak` to verify connection recovery and frame pipeline stability.
- **Hardware Testing**: Validate edge GPIO, IMU, and camera components via `python3 apps/pi-client/test_hardware.py`.

## Commit & Pull Request Guidelines
- **Commit Format**: Follow Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`). Example: `feat: add multimodal vehicle classification schema`.
- **Pull Requests**: Include a clear summary of changes, list affected packages/apps, ensure `pnpm typecheck` passes, and never commit secrets or active `.env` files.
