# Contribution Guide

## Development

現在, 開発中のために他ユーザーとのコラボレーションは検討していないが, version 0.1.0 リリース段階でコラボレーションしたい...

### Installation

```bash
pip3 install -r requirements.txt
pip3 install -r requirements-devtools.txt
pip3 install -r requirements-doctools.txt

pre-commit install
python3 setup.py develop
```

### Unit test

単体テストは [pytest](https://docs.pytest.org/en/7.1.x/) を用いて実行.

```bash
# Execute all test scripts
pytest

# If you want to execute the specified script...
pytest lpmd/tests/{specified_script_path}
```

[pytest](https://docs.pytest.org/en/7.1.x/) の使い方については以下が参考になる.

- [pytest ヘビー🐍ユーザーへの第一歩](https://www.m3tech.blog/entry/pytest-summary)
- [pytestのとりあえず知っておきたい使い方](https://qiita.com/kg1/items/4e2cae18e9bd39f014d4)

### Test for Docstring of Numpydoc

Docstring は [numpydoc](https://numpydoc.readthedocs.io/en/latest/index.html) 形式.

```bash
pydocstyle --convention=numpy .
```

[numpydoc](https://numpydoc.readthedocs.io/en/latest/index.html) 形式の書き方は以下が参考になる.

- [[Python]可読性を上げるための、docstringの書き方を学ぶ（NumPyスタイル](https://qiita.com/simonritchie/items/49e0813508cad4876b5a)

### Documents build

[sphinx](https://sphinx-users.jp/index.html) を使ってドキュメントを作成している.

```bash
# Build apidoc excluding test scripts
sphinx-apidoc -e -f -d 5 --templatedir docs/_templates/apidoc -o docs/reference/ lpmd "lpmd/tests/*"

sphinx-build -b html docs/ docs/_build/html/  
```

## Issues

工事中

## Pull Request

工事中
