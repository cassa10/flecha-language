# Trabajo Práctico Parseo y Generación de Código

- [Enunciado TP1](./docs/tp1.pdf)

- [Enunciado TP2](./docs/tp2.pdf)

Los tests se encuentran en la carpeta "./src/test":

- Tests TP1 en la carpeta "tests_parser_json".

- Tests TP2 en la carpeta "tests_interpreter".

## Pre-requirements

- python v3.11
- [PLY v3.11](https://github.com/dabeaz/ply)
- [Pytest v7.4.2](https://pypi.org/project/pytest/)
- [argparse](https://docs.python.org/3/library/argparse.html)

Note: If "py" not works use "python3" / "python".

## Docker

1) Go to repository root folder
2) Build image from Dockerfile with:

    ```bash
    docker build -t flecha .
    ```

3) Execute image as container with:

    ```bash
    docker run -it --entrypoint bash --name flecha flecha
    ```

4) Use commands in [Tests](#tests) or [Execute](#execute) sections (you might need to replace command "py" with "python3")


## Set up 


### From requirement.txt file

```bash
pip install -r requirements.txt
```

# Tests

```bash
py -m pytest -v
```

## Execute

### Help command
```bash
py ./src/main.py -h
```

### Priority

Some commands has priority. 
This means that a command which has more priority force to execute in that mode and output that mode until execution ends

#### Commands with priorities:

1- REPL (`-r`|`--repl`)
2- Tokenizer Mode (`-tM`|`--repl`)
3- Parser Mode (`-p`|`-pM`)

_Note:The priority is 1 to N where less value is more priority than a greater one_

Example: 
- command `-r` will execute as REPL.
- command `-tM` will execute as 'Tokenizer Mode' and only return all program tokens as output.
- command `-pM` will execute as 'Parser mode' and only return an ast program as output.
- command `-r -pM` will execute as REPL.
- command `-pM -tM` will execute as Tokenizer Mode.

### Enable REPL

Enables Read Evaluate Print Loop. _Note: disable all other flags_

```bash
py ./src/main.py -r
```

### Example with flag "-s" or "--stringProgram"
```bash
py ./src/main.py -s "def main = 12 * 234"
```

### Example with flag "-i" or "--inputFile"
```bash
py ./src/main.py -i "./src/test/tests_interpreter/test18.input"
```

_Note: need to be executed from root of repo_

### Example with flag "-o" or "--outputFile"

```bash
py ./src/main.py -i "./src/test/tests_interpreter/test18.input" -o "./out/test18.input"
```

_Note: need to be executed from root of repo_

### Show tokens with flags "-t" or "--tokenize"
```bash
py ./src/main.py -t -i "./src/test/tests_interpreter/test18.input"
```

### Only tokenize and return tokens with flags "-tM" or "--tokenizeMode" 
```bash
py ./src/main.py -tM -i "./src/test/tests_interpreter/test18.input"
```

### Show parsed AST with flags "-p" or "--parse" 
```bash
py ./src/main.py -p -i "./src/test/tests_interpreter/test18.input"
```

### Only parse and return parsed AST with flags "-pM" or "--parseMode" 
```bash
py ./src/main.py -pM -i "./src/test/tests_interpreter/test18.input"
```

### Enable debug info (such as: Program Input) with flags "-d" or "--debug" 
```bash
py ./src/main.py -d -p -t -i "./src/test/tests_interpreter/test18.input"
```
