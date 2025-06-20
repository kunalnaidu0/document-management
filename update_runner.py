import os
import sys
import time
import shutil
import subprocess

def main():
    # Get the old and new executable paths from command line arguments
    if len(sys.argv) < 3:
        print("Usage: update_runner.py <old_exe_path> <new_exe_path>")
        return

    old_exe = sys.argv[1]
    new_exe = sys.argv[2]

    print(f"Waiting for {old_exe} to close...")
    # Wait for the old excutable to close
    time.sleep(2)

    # Wait until old_exe is not locked
    for _ in range(10):
        try:
            # Attempt to rename the old excutable to check to see if it is locked
            os.rename(old_exe, old_exe + ".bak")
            os.rename(old_exe + ".bak", old_exe)
            break
        except Exception:
            time.sleep(1)
    else:
        print("Failed to access the old executable.")
        return

    print("Replacing old executable...")
    # Copy the new executable over the older one
    try:
        shutil.copy2(new_exe, old_exe)
        print("Update complete.")
    except Exception as e:
        print("Failed to copy new executable:", e)
        return

    # Remove downloaded file
    try:
        os.remove(new_exe)
    except Exception:
        pass

    # Write success flag
    try:
        with open(os.path.join(os.path.dirname(old_exe), "update_success.flag"), "w") as f:
            f.write("success")
    except Exception:
        pass

    print("Restarting application...")
    subprocess.Popen([old_exe])

if __name__ == "__main__":
    main()
