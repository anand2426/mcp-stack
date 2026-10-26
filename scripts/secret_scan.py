#!/usr/bin/env python3
"""
mcp-stack secret scanner.

A lightweight pre-publish grep for common secret shapes across a project
directory (tracked and untracked files), so an obvious credential doesn't
ship in a public MCP server repo. This is NOT a replacement for a real
secret-scanning tool (gitleaks, trufflehog) on a larger or long-lived repo —
it's a fast first pass for a solo project's pre-publish checklist.

Usage:
  python secret_scan.py <project-dir>

Exit code: 0 if clean, 1 if any likely secret found.
"""
import os
import re
import sys

PATTERNS = {
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "AWS access key ID": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "Generic bearer/JWT": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    "Private key block": re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}

SKIP_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", ".venv", "venv"}
TEXT_EXTENSIONS = {".js", ".ts", ".jsx", ".tsx", ".py", ".json", ".env", ".yml", ".yaml", ".md", ".txt", ".toml", ".cfg", ".ini"}


def should_scan(path):
    if os.path.basename(path).startswith(".env"):
        return True
    _, ext = os.path.splitext(path)
    return ext in TEXT_EXTENSIONS


def scan_file(path):
    findings = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for lineno, line in enumerate(f, start=1):
                for label, pattern in PATTERNS.items():
                    if pattern.search(line):
                        findings.append((path, lineno, label))
    except OSError:
        pass
    return findings


def main():
    if len(sys.argv) != 2:
        print("Usage: python secret_scan.py <project-dir>")
        sys.exit(2)

    root = sys.argv[1]
    all_findings = []
    tracked_env_files = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if filename.startswith(".env") and filename != ".env.example":
                tracked_env_files.append(full_path)
            if should_scan(full_path):
                all_findings.extend(scan_file(full_path))

    if tracked_env_files:
        print("WARNING — .env-style file(s) present (verify these are gitignored, not committed):")
        for p in tracked_env_files:
            print(f"  {p}")
        print()

    if not all_findings:
        print("PASS — no likely secrets found by pattern scan.")
        sys.exit(0)

    print(f"{len(all_findings)} likely secret(s) found:\n")
    for path, lineno, label in all_findings:
        print(f"  {path}:{lineno}  [{label}]")
    print("\nTreat each as blocking until confirmed to be a placeholder/test value, not a real credential.")
    print("If any is real: rotate it immediately and scrub it from git history before this repo goes public.")
    sys.exit(1)


if __name__ == "__main__":
    main()
