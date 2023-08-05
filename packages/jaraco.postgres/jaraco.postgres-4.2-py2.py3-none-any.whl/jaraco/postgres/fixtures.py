import pytest
import portend

from . import PostgresServer


@pytest.yield_fixture(scope="session")
def postgresql_instance():
    try:
        port = portend.find_available_local_port()
        instance = PostgresServer(port=port)
        instance.initdb()
        instance.start()
        yield instance
    except Exception as err:  # noqa: F841
        pytest.skip("Postgres not available ({err})".format(**locals()))
    instance.destroy()
