#!/usr/bin/env python3
"""Convenciones de ramas y commits de Holdpoint.

Un único sitio para las reglas, con tres usos:

  convenciones.py hook-claude        Hook PreToolUse (Bash) de Claude Code. Lee el JSON
                                     por stdin; si el comando crea una rama o hace un
                                     commit con un nombre o mensaje inválido, o hace un
                                     commit directo en main, sale con código 2 y lo
                                     explica por stderr.
  convenciones.py commit-msg <fich>  Hook commit-msg de git (lo llama .githooks/commit-msg).
  convenciones.py pre-commit         Hook pre-commit de git: bloquea los commits directos
                                     en main (los merges, no).
  convenciones.py rama <nombre>      Valida un nombre de rama (pruebas manuales).
  convenciones.py asunto <texto>     Valida el asunto de un commit (pruebas manuales).
"""

import json
import os
import re
import shlex
import subprocess
import sys

TIPOS_RAMA = ("poc", "feature", "fix", "docs", "chore", "refactor", "test", "ci")
TIPOS_COMMIT = ("feat", "fix", "docs", "chore", "refactor", "test", "ci", "build", "perf")
MAX_ASUNTO = 72
RAMA_PROTEGIDA = "main"
# Salida de emergencia, solo para una persona en su terminal: el hook de Claude Code
# bloquea cualquier comando que la mencione.
VAR_PERMITIR_MAIN = "HOLDPOINT_PERMITIR_MAIN"

RE_RAMA = re.compile(
    r"^(main"
    r"|feature/entrega-[0-9]+-fp"
    r"|(" + "|".join(TIPOS_RAMA) + r")/([0-9]+-)?[a-z0-9]+(-[a-z0-9]+)*"
    r")$"
)
RE_ASUNTO = re.compile(
    r"^(" + "|".join(TIPOS_COMMIT) + r")(\([a-z0-9][a-z0-9-]*\))?!?: (?P<desc>\S.*)$"
)
# Mensajes que genera git y no se tocan.
RE_ASUNTO_GIT = re.compile(r"^(Merge |Revert \"|fixup! |squash! |amend! )")

AYUDA_RAMA = (
    "Formato de rama: main, feature/entrega-N-fp o <tipo>/<slug-en-kebab-case>\n"
    f"  tipos: {', '.join(TIPOS_RAMA)}\n"
    "  número de Issue opcional al principio del slug\n"
    "  ejemplos: poc/pasarela, feature/12-registrar-servidor, docs/arquitectura"
)
AYUDA_COMMIT = (
    "Formato de commit (Conventional Commits en español):\n"
    "  <tipo>(<ámbito opcional>): <descripción>\n"
    f"  tipos: {', '.join(TIPOS_COMMIT)}\n"
    f"  descripción en minúscula, sin punto final; asunto de {MAX_ASUNTO} caracteres como máximo\n"
    "  ejemplo: docs(arnes): añade CLAUDE.md y registro de IA\n"
    "  Refs #n del Issue en el cuerpo, si aplica"
)

AYUDA_MAIN = (
    f"No se commitea directamente en {RAMA_PROTEGIDA}: crea una rama (<tipo>/<slug>), haz ahí el\n"
    f"commit e intégrala con «git merge --no-ff <rama>» (sin pull request). Los merges sí se permiten."
)


def error_rama(nombre):
    """Devuelve el motivo del rechazo, o None si el nombre es válido."""
    if RE_RAMA.match(nombre):
        return None
    return f"Rama «{nombre}» no válida.\n{AYUDA_RAMA}"


def error_asunto(asunto):
    """Devuelve el motivo del rechazo, o None si el asunto es válido."""
    if RE_ASUNTO_GIT.match(asunto):
        return None
    if len(asunto) > MAX_ASUNTO:
        return f"El asunto tiene {len(asunto)} caracteres (máximo {MAX_ASUNTO}).\n{AYUDA_COMMIT}"
    m = RE_ASUNTO.match(asunto)
    if not m:
        return f"Asunto «{asunto}» no válido.\n{AYUDA_COMMIT}"
    desc = m.group("desc")
    if desc[0].isupper():
        return f"La descripción empieza en mayúscula: «{desc}».\n{AYUDA_COMMIT}"
    if desc.endswith("."):
        return f"La descripción termina en punto: «{desc}».\n{AYUDA_COMMIT}"
    return None


def git(args, cwd=None):
    """Salida de un comando git, o None si falla (no es un repo, git no instalado...)."""
    try:
        r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def en_rama_protegida(cwd=None):
    return git(["rev-parse", "--abbrev-ref", "HEAD"], cwd) == RAMA_PROTEGIDA


def merge_en_curso(cwd=None):
    """Un commit que cierra un merge con conflictos es legítimo en main."""
    return git(["rev-parse", "-q", "--verify", "MERGE_HEAD"], cwd) is not None


# --- Análisis de comandos de shell -------------------------------------------------

SEPARADORES = {"&&", "||", ";", "|", "&", "\n", "(", ")", ";;", "|&"}


def segmentos(comando):
    """Parte un comando de shell en comandos simples (listas de tokens)."""
    lex = shlex.shlex(comando, posix=True, punctuation_chars="();<>|&\n")
    lex.whitespace = " \t\r"
    lex.whitespace_split = True
    actual, todos = [], []
    for tok in lex:
        if tok in SEPARADORES or set(tok) <= set("();|&\n"):
            if actual:
                todos.append(actual)
            actual = []
        else:
            actual.append(tok)
    if actual:
        todos.append(actual)
    return todos


def subcomando_git(tokens):
    """Si el comando es git, devuelve (subcomando, argumentos); si no, None."""
    # Saltar asignaciones de entorno (VAR=x git ...)
    i = 0
    while i < len(tokens) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[i]):
        i += 1
    if i >= len(tokens) or tokens[i].rsplit("/", 1)[-1] != "git":
        return None
    i += 1
    while i < len(tokens) and tokens[i].startswith("-"):
        if tokens[i] in ("-C", "-c", "--git-dir", "--work-tree", "--namespace"):
            i += 2
        else:
            i += 1
    if i >= len(tokens):
        return None
    return tokens[i], tokens[i + 1:]


def ramas_creadas(sub, args):
    """Nombres de rama que crea o renombra el comando git."""
    nombres = []
    if sub == "checkout":
        for j, a in enumerate(args):
            if a in ("-b", "-B", "--orphan") and j + 1 < len(args):
                nombres.append(args[j + 1])
    elif sub == "switch":
        for j, a in enumerate(args):
            if a in ("-c", "-C", "--create", "--force-create", "--orphan") and j + 1 < len(args):
                nombres.append(args[j + 1])
            elif a.startswith(("--create=", "--force-create=")):
                nombres.append(a.split("=", 1)[1])
    elif sub == "worktree" and args and args[0] == "add":
        for j, a in enumerate(args):
            if a in ("-b", "-B") and j + 1 < len(args):
                nombres.append(args[j + 1])
    elif sub == "branch":
        solo_consulta = {
            "-d", "-D", "--delete", "-l", "--list", "-a", "--all", "-r", "--remotes",
            "--show-current", "-v", "-vv", "--verbose", "--contains", "--no-contains",
            "--merged", "--no-merged", "--points-at", "-u", "--set-upstream-to",
            "--unset-upstream", "--edit-description", "--format", "--sort",
        }
        if any(a in solo_consulta or a.startswith(("--set-upstream-to=", "--format=", "--sort="))
               for a in args):
            return []
        renombra = any(a in ("-m", "-M", "-c", "-C", "--move", "--copy") for a in args)
        posicionales = [a for a in args if not a.startswith("-")]
        if renombra and posicionales:
            nombres.append(posicionales[-1])
        elif posicionales:
            nombres.append(posicionales[0])
    return nombres


def mensaje_commit(args):
    """Primer mensaje pasado con -m; None si no hay o no se puede leer (heredoc, -F...)."""
    for j, a in enumerate(args):
        if a in ("-m", "--message"):
            return args[j + 1] if j + 1 < len(args) else None
        if a.startswith("--message="):
            return a.split("=", 1)[1]
        if a.startswith("-") and not a.startswith("--") and "m" in a[1:]:
            resto = a[a.index("m", 1) + 1:]
            if resto:
                return resto
            return args[j + 1] if j + 1 < len(args) else None
    return None


def revisar_comando(comando, cwd=None):
    """Lista de errores de convención en un comando de shell."""
    errores = []
    if VAR_PERMITIR_MAIN in comando:
        return [f"El comando menciona {VAR_PERMITIR_MAIN}: esa salida de emergencia es solo "
                f"para una persona en su terminal.\n{AYUDA_MAIN}"]
    try:
        partes = segmentos(comando)
    except ValueError:
        # Comillas sin cerrar o heredoc: búsqueda aproximada de ramas;
        # el commit lo valida el hook commit-msg de git.
        for m in re.finditer(r"git\s+(?:checkout\s+-[bB]|switch\s+-[cC])\s+([^\s;&|]+)", comando):
            e = error_rama(m.group(1).strip("'\""))
            if e:
                errores.append(e)
        return errores
    rama_incierta = False  # tras un checkout/switch no se sabe en qué rama se hace el commit
    for tokens in partes:
        r = subcomando_git(tokens)
        if not r:
            continue
        sub, args = r
        if sub in ("checkout", "switch", "worktree", "reset", "rebase"):
            rama_incierta = True
        if (sub == "commit" and not rama_incierta and en_rama_protegida(cwd)
                and not merge_en_curso(cwd)):
            errores.append(AYUDA_MAIN)
        for nombre in ramas_creadas(sub, args):
            e = error_rama(nombre)
            if e:
                errores.append(e)
        if sub == "commit":
            msg = mensaje_commit(args)
            if msg is None or "$(" in msg or "`" in msg:
                continue
            asunto = msg.strip().splitlines()[0] if msg.strip() else ""
            e = error_asunto(asunto)
            if e:
                errores.append(e)
    return errores


# --- Puntos de entrada --------------------------------------------------------------

def hook_claude():
    try:
        datos = json.load(sys.stdin)
        comando = datos.get("tool_input", {}).get("command", "")
        cwd = datos.get("cwd") or None
    except Exception:
        return 0  # Si no se puede leer la entrada, no se bloquea.
    errores = revisar_comando(comando, cwd)
    if errores:
        print("Bloqueado por las convenciones del repo (ver CLAUDE.md):\n"
              + "\n\n".join(errores), file=sys.stderr)
        return 2
    return 0


def commit_msg(fichero):
    with open(fichero, encoding="utf-8") as f:
        lineas = [l.rstrip("\n") for l in f if not l.startswith("#")]
    asunto = next((l.strip() for l in lineas if l.strip()), "")
    e = error_asunto(asunto)
    if e:
        print(e, file=sys.stderr)
        return 1
    return 0


def pre_commit():
    if os.environ.get(VAR_PERMITIR_MAIN) == "1":
        return 0
    if en_rama_protegida() and not merge_en_curso():
        print(AYUDA_MAIN, file=sys.stderr)
        return 1
    return 0


def main(argv):
    if len(argv) >= 2 and argv[1] == "hook-claude":
        return hook_claude()
    if len(argv) == 2 and argv[1] == "pre-commit":
        return pre_commit()
    if len(argv) == 3 and argv[1] == "commit-msg":
        return commit_msg(argv[2])
    if len(argv) == 3 and argv[1] in ("rama", "asunto"):
        e = (error_rama if argv[1] == "rama" else error_asunto)(argv[2])
        print(e or "OK", file=sys.stderr if e else sys.stdout)
        return 1 if e else 0
    print(__doc__, file=sys.stderr)
    return 64


if __name__ == "__main__":
    sys.exit(main(sys.argv))
