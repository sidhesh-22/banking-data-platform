import subprocess
import sys

SCRIPTS = [
    "customers.py",
    "merchants.py",
    "accounts.py",
    "cards.py",
    "transactions.py"
]


def run_script(script):

    print("\n" + "=" * 60)
    print(f"Running {script}...")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, script]
    )

    if result.returncode != 0:

        print(f"\n❌ {script} failed.")
        sys.exit(1)

    print(f"✅ {script} completed successfully.")


def main():

    for script in SCRIPTS:
        run_script(script)

    print("\n" + "=" * 60)
    print("🎉 ALL DATA GENERATED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()

