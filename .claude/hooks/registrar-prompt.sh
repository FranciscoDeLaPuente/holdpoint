#!/usr/bin/env bash
# Hook UserPromptSubmit: añade cada prompt a .registro-ia/AAAA-MM-DD.jsonl.
# No escribe nada por stdout/stderr (en este hook la salida se añade al contexto)
# y siempre termina con 0 para no bloquear nunca el prompt.
{
  entrada=$(cat)
  raiz="${CLAUDE_PROJECT_DIR:-$(printf '%s' "$entrada" | jq -r '.cwd // empty')}"
  [ -n "$raiz" ] || raiz="$PWD"
  dir="$raiz/.registro-ia"
  mkdir -p "$dir"
  rama=$(git -C "$raiz" branch --show-current 2>/dev/null)
  printf '%s' "$entrada" | jq -c \
    --arg fecha "$(date -Iseconds)" \
    --arg rama "$rama" \
    '{fecha: $fecha, rama: $rama, sesion: .session_id, transcripcion: .transcript_path, prompt: .prompt}' \
    >> "$dir/$(date +%F).jsonl"
} >/dev/null 2>&1
exit 0
