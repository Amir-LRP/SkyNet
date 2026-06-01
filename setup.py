"""
SKYNET Setup Script
Installs all dependencies and Playwright browsers.
"""
import subprocess
import sys

print("=" * 50)
print("  SKYNET — Autonomous AI Operating System")
print("  Setup & Dependency Installer")
print("=" * 50)
print()

print("[1/2] Installing Python dependencies...")
subprocess.run(
    [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
    check=True,
)

print()
print("[2/2] Installing Playwright browsers...")
subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)

print()
print("=" * 50)
print("  ✅ Setup complete.")
print("  Run: python main.py")
print("=" * 50)
