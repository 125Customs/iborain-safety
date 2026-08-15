# Build from monorepo root: docker build -f apps/backend/Dockerfile .
FROM node:22-slim AS build
RUN corepack enable
WORKDIR /repo
COPY pnpm-workspace.yaml package.json tsconfig.base.json ./
COPY packages/protocol/package.json packages/protocol/
COPY apps/backend/package.json apps/backend/
RUN pnpm install --no-frozen-lockfile
COPY packages/protocol packages/protocol
COPY apps/backend apps/backend
RUN pnpm --filter @pixel-bot/protocol build && pnpm --filter @pixel-bot/backend build

FROM node:22-slim
RUN corepack enable
WORKDIR /repo
ENV NODE_ENV=production
COPY --from=build /repo ./
EXPOSE 8080
CMD ["node", "apps/backend/dist/src/index.js"]
