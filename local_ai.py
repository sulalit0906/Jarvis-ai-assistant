import subprocess

def ask_local_ai(question):

    result = subprocess.run(
        [
            "ollama",
            "run",
            "phi3:latest",
            question
        ],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    return result.stdout.strip()
