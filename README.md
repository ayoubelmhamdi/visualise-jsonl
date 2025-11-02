# datasets/jsonl creating Status Checker

Checks the status of `input.md`, `metadata.md`, and `output.md` files in directory trees.

## Status Indicators
- 🟩 Green (`A`): File exists and is non-empty
- 🟨 Yellow (`B`): File exists but is empty
- 🟥 Red (`C`): File does not exist

## Setup

Create `input.txt` with directories to check:


```
datasete/s5/examens/2010
datasete/s5/serie_6
```

## Testing

Create test directories and files:
```
mkdir -p datasete/s5/examens/2010/{exercice,prob1}
mkdir -p datasete/s5/serie_6/{exercice1/{1,2},ex2/{prob,qcm},exercice2/{1,3},ex1/{prob,qcm}}

touch datasete/s5/examens/2010/exercice/{input.md,metadata.md}
touch datasete/s5/serie_6/exercice1/2/{input.md,output.md}
touch datasete/s5/serie_6/ex1/prob/{input.md,output.md}

echo "content" > datasete/s5/examens/2010/exercice/input.md
echo "content" > datasete/s5/serie_6/exercice1/2/input.md
```

## Usage

```
python3 main.py
```

Output shows a tree view with colored status boxes for each directory's three files.
