import subprocess


def execute_build_ebase_command(*, command: str, timeout_seconds=10):
    print("build ebase...START")
    try:
        shlex_command = command.split()
        completed_process = subprocess.run(
            shlex_command, check=True, timeout=timeout_seconds
        )
        complete_message = "SUCCESS" if completed_process.returncode == 0 else "FAILED"
        print(f"Complete: {completed_process}")
        code = completed_process.returncode
        if code == 0:
            print(f"build ebase... [{code}] {complete_message}")
        else:
            print(f"build ebase... [{code}] {complete_message}")
    except Exception as e:
        print(f"build ebase...FAILED with Exception: {e}")
