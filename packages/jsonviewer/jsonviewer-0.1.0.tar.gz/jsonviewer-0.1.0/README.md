# jsonviewer
print meta json structure

## Install
```
pip install jsonviewer
```

## Usage
```
from jsonviewer import view_json

fname = "foo.json"
with open(fname) as f:
	data = json.load(f)
view_json(data)
```


