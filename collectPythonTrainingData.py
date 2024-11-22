# Compile python scripts data under data/repo into a single file and prepare it for tokenization.
# I briefly considered doing this as a shell script... but this is much better (worse).

# Launch options include:
# --search  ->  Grabs a list of repos from github using list of search queries. Run "gh-auth login" in advance to store credentials.
# --fetch   ->  Clones all repos from the latest repo_urls_*.txt
# --prepare ->  Attempts to rid all of the non utf-8 characters that exist in data/repo/*.py files using removebadchar.sh
# --format  ->  Attempts to use black to normalize python files in data/repo/. This takes a /long/ time and many files will fail.
# --clean   ->  Remove data/repo after compilation

import os
import sys
from datetime import datetime as dt
from git import Repo
from shutil import rmtree

time = dt.now().isoformat()

# Search querys for repo's in GitHub
queries = [
  "python3 leetcode solutions",
  "algorithm explanation python3",
  "python3 examples",
]

def fetchSearchResults():
  # The search will be sorted by stars and hopefully include results written in python.
  # I'm not sure if language:en has any affect on producing english results or not.
  urls = []
  file_name = f"data/python-trainingData/repo_urls_{time}.txt"

  for q in queries:
    command = f"gh api search/repositories --method=GET -F q='{q} language:python language:en sort:stars' --paginate --jq '.items[].html_url' >> {file_name}"
    os.system(command)

  with open(file_name) as file:
    for line in file:
      urls.append(line.strip())
  
  return urls

def cloneRepos(urls):
  # Clone each of the repos in urls to ./data/repo/{username}/{repo name}/
  for r in urls:
    try:
      Repo.clone_from(r, f"./data/repo/{r[19:]}")
    except Exception as e:
      print(e)
      pass

def preparePythonFiles():
  # Prepare python files for compilation.
  # Remove any non utf-8
  os.system("bash removebadchar.sh")
  # TODO: Sometimes there are zero-width spaces (U+200B) and null bytes (U+0000) left in the files.

def formatPythonFiles():
  # align python formatting across file
  for parent, subdirs, files in os.walk("data/repo/"):
    for f in files:
      if f[-3:] == ".py":
        path = os.path.join(parent, f)
        os.system(f"black '{path}'")

def compileTrainingData():
  # Generate one big python file from the repos.
  trainingDataPath = f"./data/python-trainingData/trainingData_{time}.py"

  with open(trainingDataPath, "w") as output_file:
    for parent, subdirs, files in os.walk("data/repo/"):
      for f in files:
        if f[-3:] == ".py":
          path = os.path.join(parent, f)
          try:
            with open(path) as input_file:
              for line in input_file:
                output_file.write(line)
          except Exception as e:
            print(e)
            continue
          output_file.write("\n")
  
  return trainingDataPath

if __name__ == '__main__':
  if '--search' in sys.argv:
    urls = fetchSearchResults()
  else:
    urls_txt = []
    urls = []
    for file in os.listdir("data/python-trainingData/"): # Find latest search results and pull urls from there.
      if file[:10] == 'repo_urls_':
        urls_txt.append(file)
    if len(urls_txt) > 0:
      with open(os.path.join("data/python-trainingData/", urls_txt[-1])) as file:
        for line in file:
          urls.append(line.strip())

  if '--fetch' in sys.argv:
    if len(urls) > 0:
      cloneRepos(urls)
    else:
      print("Cannot fetch without --search flag or existing search results")

  if '--prepare' in sys.argv:
    preparePythonFiles()
  
  if '--format' in sys.argv:
    formatPythonFiles()

  compileTrainingData()

  if '--clean' in sys.argv:
    rmtree("./data/repo/")
