import subprocess
import json
import os


class OSVRunner:
    def run(self, repo_path: str) -> dict:
        """
        Runs osv-scanner against a repository directory and returns raw JSON output.

        Assumptions:
        - osv-scanner is installed and available on PATH
        - repo_path is a local filesystem path
        """

        cmd = [
            "osv-scanner",
            "scan",
            "--recursive",
            "--format", "json",
            repo_path
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        # osv-scanner exit codes:
        # 0 → no vulnerabilities
        # 1 → vulnerabilities found
        if result.returncode not in (0, 1):
            raise RuntimeError(
                f"OSV-Scanner failed.\nSTDERR:\n{result.stderr}"
            )

        # Defensive: osv-scanner may emit empty output if nothing is detected
        if not result.stdout.strip():
            return {"results": []}

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                f"OSV-Scanner produced invalid JSON.\n"
                f"STDOUT:\n{result.stdout}\n\n"
                f"STDERR:\n{result.stderr}"
            ) from e
