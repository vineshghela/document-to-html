# docx to HTML tool

## dependencies

## How to get started
please make sure you have `python 3.10+` this can be checked by running `python3 --version`

### File/software needed for this to work 
- pandoc
- clean_md.py
- clean_html.py


1. first create a new virtual environment and activate it
```bash
python3 -m venv myenv 
source myenv/bin/activate  
```

2. Next install the dependencies
```bash
 sudo apt-get update                                                                               ✘ INT 🐍 myenv 02:31:55 pm
 sudo apt-get install pandoc
 pip install -r requirements.txt
```


3. Then in the directory files add you `.docx` file  
4. Then run the following command in the terminal. The convert the `.docx` to a `markdown` document
```bash
pandoc -s files/Debenture.docx -t markdown -o output.md
```

5. Now its worth checking the `output.md` to see if there is anything that you can fix e.g. (note this can be done after step 6 also)
    1. Headers
    2. Lists

6. now run the following 

```bash
python clean_md.py
# This will delete the output.md and create a new file called output_cleaned.md
# At this point its worth repeating step 5 and just checking
```

7. Now we need to convert the `md` to `html`
```bash
pandoc -s output_cleaned.md -o output.html
```
8. Now we run 
```bash
python clean_html
# this removes any ids, classes or weird syntax e.g. {}
# this will delete the old output.md file
```

9. Finally the finished product will be `output_cleaned.html`
