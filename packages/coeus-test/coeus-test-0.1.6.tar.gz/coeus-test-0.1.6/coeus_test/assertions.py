import commands

default_parameters = {}


def assert_verify_message(message):
    """
    Verifies that the message is not None,
    'payload' exists and 'payload' is not None.
    :param message:
    :return:
    """
    assert message is not None
    assert 'payload' in message
    assert message['payload'] is not None


def assert_entity_is_registered(cli, entity_id):
    """
    Asserts that the entity is registered.
    :param cli:
    :param entity_id:
    :return:
    """
    result = commands.query_entity_is_registered(cli, entity_id)
    assert_verify_message(result)
    assert result['payload']['result'] is True
    return result


def assert_await_entity_registered(cli, entity_id, is_registered=True, timeout_seconds=60):
    """
    Asserts that we successfully awaited for the registration state of the entity. If the timeout passes
    or the expression is_registered != actual state, then it will fail.
    :param cli:
    :param entity_id:
    :param is_registered: (True | False) the state change we are waiting for.
    :param timeout_seconds: The amount of time to wait for a change before fail.
    :return:
    """
    result = commands.await_entity_registered(cli, entity_id, is_registered, timeout_seconds)
    assert_verify_message(result)
    assert result['payload']['success'] is True
    return result


def assert_invoke_entity_method(cli, entity_id, method_name, parameters=default_parameters):
    """
    Asserts that the invocation has not errored.
    :param cli:
    :param entity_id:
    :param method_name: The public method name we are invoking
    :param parameters: A {} of values to pass to the method. Converted to IDynamicObject.
    :return:
    """
    result = commands.invoke_entity_method(cli, entity_id, method_name, parameters)
    assert_verify_message(result)
    assert result['payload']['is_error'] is False, result['payload']['error_message']
    return result


def assert_fetch_entity(cli, entity_id):
    """
    Asserts that the returned test_entity is not None.
    :param cli:
    :param entity_id:
    :return:
    """
    result = commands.fetch_entity(cli, entity_id)
    assert_verify_message(result)
    assert result['payload']['test_entity'] is not None
    return result
