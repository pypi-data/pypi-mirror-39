# Coeus-Unity

[pypi-build-status]: https://img.shields.io/pypi/v/coeus-test-unity.svg
[travis-ci-status]: https://img.shields.io/travis/AgeOfLearning/coeus-unity-python-framework.svg

[![pypi][pypi-build-status]](https://pypi.python.org/pypi/coeus-test-unity)
[![travis][travis-ci-status]](https://travis-ci.org/AgeOfLearning/coeus-unity-python-framework)

## About
Coeus-Unity is a collection of commands and assertions built on `coeus-test` package for python. These commands support remote integration tests in Unity with the use of the C# Coeus test framework.

## Setup
Simply install the requirement into your package.

```python
pip install coeus-test-unity
```

## Commands
Commands offer no response validation. You can use assertions for that.

```python
import commands

response = commands.query_transform_exists(cli, "My/Transform Hierarchy/Object (Clone)")
response = commands.query_scene_loaded(cli, "AppSetup")
response = commands.query_renderer_visible(cli, "My/Target/Object (Clone)")

response = commands.await_transform_exists(cli, "My/Transform Hierarchy/Object (Clone)")
# Waits for renderer to become not visible based on False...
response = commands.await_renderer_visible(cli, "My/Transform Hierarchy/Object (Clone)", False)
response = commands.await_scene_loaded(cli, "AppSetup")
```