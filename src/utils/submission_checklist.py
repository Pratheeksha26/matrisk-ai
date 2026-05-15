import os
import sys

# Ensure the root directory is in the python path
sys.path.append(os.getcwd())

def check_submission_readiness():
    """
    Verify all required files and configurations are present for final submission.
    """
    requirements = [
        "README.md",
        "LICENSE",
        "Makefile",
        "requirements.txt",
        ".env.example",
        "docker-compose.yml",
        ".github/workflows/ci.yml",
        "docs/technical_report_skeleton.md",
        "src/dashboard/app.py",
        "src/models/train_model.py",
        "tests/test_integration.py"
    ]
    
    missing = []
    for req in requirements:
        if not os.path.exists(req):
            missing.append(req)
            
    if not missing:
        print("[SUCCESS]: All mandatory files detected. Repository is ready for transfer.")
    else:
        print("[FAILED]: Mandatory files missing:")
        for m in missing:
            print(f"  - {m}")

            
    return len(missing) == 0

if __name__ == "__main__":
    check_submission_readiness()
