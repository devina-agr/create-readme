import os
import json
import requests
from config import API_KEY
# from dotenv import load_dotenv
#
# load_dotenv()
# api_key = os.getenv("API_KEY")


def create_readme(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for i in filenames:
            files.append(os.path.join(root, i))  

    file_data = []
    for path in files:

        with open(path, "r") as reader:
            data = reader.read()

        file_data.append(
            {
                "path": path,  # stores the path of the file
                "size": os.path.getsize(
                    path
                ),  # returns the size of the file at that path
                "modified": os.path.getmtime(
                    path
                ),  # returns the time it was last modified
                "data": data,
            }
        )

    prompt = f"Generate a clean, concise, and easy to understand readme file in markdown format for a project with the following files:\n\n{json.dumpd(file_data, indent=4)}"

    ai_response = requests.post(
        "https://api.gemini.com/generate",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"prompt": prompt},
    )

    if ai_response.status_code == 200:
        readme_content = ai_response.json()["text"]
        with open("README.md", "w") as f:
            f.write(readme_content)
        print("README file generated successfully!")
    else:
        print("Error generating README file:\n", ai_response.text)


if __name__ == "__main__":
    directory = input("Enter the directory path (input 'cd' for current directory: ")
    if directory == "cd":
        directory = os.getcwd()

    create_readme(directory)
