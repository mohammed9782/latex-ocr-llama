#!/bin/sh
set -e

# wait-and-pull.sh
# Waits for the ollama server to be reachable, then pulls the given model.
# Exits with non-zero on timeout.

MODEL=${MODEL:-llama3.2-vision}
MAX=${MAX:-60} # max attempts (with 2s sleep => ~120s)
i=0

echo "wait-and-pull: waiting for ollama server to be ready... (model=${MODEL})"
until ollama list >/dev/null 2>&1; do
  i=$((i+1))
  echo "wait-and-pull: waiting for ollama server... ($i)"
  sleep 2
  if [ "$i" -ge "$MAX" ]; then
    echo "wait-and-pull: timeout waiting for ollama after $((MAX*2)) seconds"
    exit 1
  fi
done

echo "wait-and-pull: server ready — pulling model ${MODEL}"
ollama pull "$MODEL"
echo "wait-and-pull: pull finished"
