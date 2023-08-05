# Coeus-Unity

[pypi-build-status]: https://img.shields.io/pypi/v/coeus-test-unity.svg
[travis-ci-status]: https://img.shields.io/travis/AgeOfLearning/coeus-unity-python-framework.svg

[![pypi][pypi-build-status]](https://pypi.python.org/pypi/coeus-test-unity)
[![travis][travis-ci-status]](https://travis-ci.org/AgeOfLearning/coeus-unity-python-framework)


## About
Coeus-Unity is a collection of commands and assertions built on `coeus-test` package for python. These commands support remote integration tests in Unity with the use of the C# Coeus test framework.

### Contributors
- [@dklompmaker](https://github.com/dklompmaker)
- [@copyleftdev](https://github.com/copyleftdev)
- [@KeithPatch](https://github.com/KeithPatch)

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

# Finds a FieldInfo | PropertyInfo on the component and attempts to assign the value (String | Number | Boolean)
commands.assign_component_value(cli, "My/Transform/Target", "Text", "text", "Hello World")
```

## Assertions
Since commands only assert the response message, they don't verify the state being requested; for this we can use the assertions.

```python
import assertions

# Fails immediately if transform doesn't exist...
assertions.assert_transform_exists(cli, "Some/Path")

# Fails immediately if scene not loaded...
assertions.assert_scene_loaded(cli, "MyScene")

# Awaits for the scene to be loaded, fails when exceeded...
assertions.assert_await_scene_loaded(cli, "MyScene")

# Awaits for a transform to exist by timeout, fails when exceeded...
assertions.assert_await_transform_exists(cli, "Some/Path", timeout_seconds=10)

# Awaits for a renderer to be visible by timeout, fails when exceeded...
assertions.assert_await_renderer_visible(cli, "Some/Path", timeout_seconds=10)

# Awaits for all transforms to exist by timeout, fails when exceeded...
assertions.assert_await_all_transforms_exist(cli, ["Some/Path1", "Some/Path2"], timeout_seconds=10)

# Awaits for any of the transforms to exist by timeout, fails when exceeded...
assertions.assert_await_any_transforms_exist(cli, ["Some/Path1", "Some/Path2"], timeout_seconds=10)
```

## Advanced

### Transform Path Variables
If your client supports variable replacement, you can simply pass them into your paths. For instance if you have different variations on transform path names based on some predictable variable, you can pass those in for replacement.

```python
# {deviceFormfactor} is replaced in client...
assertions.assert_await_transform_exists(cli, "Kiosk-{deviceFormFactor}(Clone"), timeout_seconds=10)
```