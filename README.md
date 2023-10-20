# Trabajo Práctico Parseo y Generación de Código

[Enunciado TP1](./docs/tp1.pdf)

## Pre-requisitos

- python v3.11
- [PLY v3.11](https://github.com/dabeaz/ply)
- [Pytest v7.4.2](https://pypi.org/project/pytest/)
- [argparse](https://docs.python.org/3/library/argparse.html)


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


### Example with flag "-s" or "--stringProgram"
```bash
py ./src/main.py -s 12+234
```

### Example with flag "-i" or "--inputFile"
```bash
py ./src/main.py -i test/tests_parser_json/test18.input
```

### Show tokens with flags "-t" or "--tokenize"
```bash
py ./src/main.py -t -i test/tests_parser_json/test18.input
```

### Enable debug info (such as: Program Input) with flags "-d" or "--debug" 
```bash
py ./src/main.py -d -t -i test/tests_parser_json/test18.input
```