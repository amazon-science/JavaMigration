"""Shell tool with restricted access for safe command execution."""

import os
import re
import subprocess

from strands import tool


def create_restricted_shell(allowed_path: str):
    """
    Create a shell tool that only executes commands within allowed_path.

    Args:
        allowed_path: The directory path where commands are allowed to execute

    Returns:
        A Strands tool that executes shell commands with path restrictions
    """
    allowed_path = os.path.abspath(allowed_path)

    def is_path_within_allowed(path: str) -> bool:
        """Check if a path resolves to within the allowed directory."""
        # Handle paths relative to allowed_path
        if not os.path.isabs(path):
            full_path = os.path.normpath(os.path.join(allowed_path, path))
        else:
            full_path = os.path.normpath(path)
        return full_path.startswith(allowed_path)

    def validate_command(command: str) -> tuple[bool, str]:
        """Validate command doesn't try to escape the allowed path."""
        # Pattern to find cd commands with their target directory
        cd_pattern = r"\bcd\s+([^\s;&|]+)"

        for match in re.finditer(cd_pattern, command):
            target = match.group(1).strip("\"'")

            # Skip special cases
            if target in ["-", "~"]:
                return False, f"Error: 'cd {target}' is not allowed in restricted shell"

            # Check if the cd target escapes allowed path
            if not is_path_within_allowed(target):
                return (
                    False,
                    f"Error: 'cd {target}' would escape the allowed path '{allowed_path}'",
                )

        # Block absolute paths to sensitive locations in other commands
        # Look for absolute paths that are outside allowed_path
        abs_path_pattern = r"(?<![\"'])\s(/[^\s;&|*?]+)"
        for match in re.finditer(abs_path_pattern, command):
            path = match.group(1)
            # Allow paths within the allowed directory
            if path.startswith(allowed_path):
                continue
            # Allow common safe system paths for tools
            safe_prefixes = ["/usr/bin/", "/bin/", "/usr/local/bin/", "/dev/null", "/tmp"]
            if any(path.startswith(p) for p in safe_prefixes):
                continue
            # Block other absolute paths
            return (
                False,
                f"Error: Absolute path '{path}' is outside the allowed path '{allowed_path}'",
            )

        return True, ""

    @tool
    def restricted_shell(command: str) -> str:
        """
        Execute shell commands within the restricted repository path.

        Args:
            command: The shell command to execute

        Returns:
            Command output (stdout and stderr combined)
        """
        # Validate the command doesn't try to escape
        is_valid, error_msg = validate_command(command)
        if not is_valid:
            return error_msg

        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=allowed_path,
                capture_output=True,
                text=True,
                timeout=300,
            )
            output = result.stdout + result.stderr
            return output if output else "(no output)"
        except subprocess.TimeoutExpired:
            return "Error: Command timed out after 300 seconds"
        except Exception as e:
            return f"Error executing command: {str(e)}"

    return restricted_shell
