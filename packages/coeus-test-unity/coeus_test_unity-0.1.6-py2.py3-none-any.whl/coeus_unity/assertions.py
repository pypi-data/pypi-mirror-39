import commands

DEFAULT_TIMEOUT_SECONDS = 60
DEFAULT_TRANSFORM_EXISTS = True
DEFAULT_RENDERER_VISIBLE = True
DEFAULT_SCENE_LOADED = True


def assert_transform_exists(cli, transform_path):
    """
    Asserts that the transform exists.
    :param cli:
    :param transform_path:
    :return:
    """
    result = commands.query_transform_exists(cli, transform_path)
    assert result is True
    return result


def assert_scene_loaded(cli, scene_name):
    """
    Asserts that the scene is loaded.
    :param cli:
    :param scene_name:
    :return:
    """
    result = commands.query_scene_loaded(cli, scene_name)
    assert result is True
    return result


def assert_await_transform_exists(cli, transform_path, does_exist=DEFAULT_TRANSFORM_EXISTS, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Asserts that we successfully awaited for the transform to exist based on does_exist. If the timeout passes
    or the expression is_registered != actual state, then it will fail.
    :param cli:
    :param transform_path:
    :param does_exist: (True | False) the state change we are waiting for.
    :param timeout_seconds: The amount of time to wait for a change before fail.
    :return:
    """
    result = commands.await_transform_exists(cli, transform_path, does_exist, timeout_seconds)
    assert result is True
    return result


def assert_await_any_transforms_exist(cli, transform_paths, does_exist=DEFAULT_TRANSFORM_EXISTS, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Asserts that we successfully awaited for any transforms to exist based on does_exist. If the timeout passes
    or the expression is_registered != actual state, then it will fail.
    :param cli:
    :param transform_paths:
    :param does_exist: (True | False) the state change we are waiting for.
    :param timeout_seconds: The amount of time to wait for a change before fail.
    :return:
    """
    result = commands.await_any_transforms_exist(cli, transform_paths, does_exist, timeout_seconds)
    assert result is True
    return result


def assert_await_all_transforms_exist(cli, transform_paths, does_exist=DEFAULT_TRANSFORM_EXISTS, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Asserts that we successfully awaited for all transforms to exist based on does_exist. If the timeout passes
    or the expression is_registered != actual state, then it will fail.
    :param cli:
    :param transform_paths:
    :param does_exist: (True | False) the state change we are waiting for.
    :param timeout_seconds: The amount of time to wait for a change before fail.
    :return:
    """
    result = commands.await_all_transforms_exist(cli, transform_paths, does_exist, timeout_seconds)
    assert result is True
    return result


def assert_await_renderer_visible(cli, transform_path, is_visible=DEFAULT_RENDERER_VISIBLE, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Asserts that we successfully awaited for the renderer to be visible based on is_visible. If the timeout passes
    or the expression is_registered != actual state, then it will fail.
    :param cli:
    :param transform_path:
    :param is_visible: (True | False) the state change we are waiting for.
    :param timeout_seconds: The amount of time to wait for a change before fail.
    :return:
    """
    result = commands.await_renderer_visible(cli, transform_path, is_visible, timeout_seconds)
    assert result is True
    return result


def assert_await_scene_loaded(cli, scene_name, is_loaded=DEFAULT_SCENE_LOADED, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Asserts that we successfully awaited for the scene to be loaded based on is_loaded. If the timeout passes
    or the expression is_registered != actual state, then it will fail.
    :param cli:
    :param scene_name:
    :param is_loaded: (True | False) the state change we are waiting for.
    :param timeout_seconds: The amount of time to wait for a change before fail.
    :return:
    """
    result = commands.await_scene_loaded(cli, scene_name, is_loaded, timeout_seconds)
    assert result is True
    return result
