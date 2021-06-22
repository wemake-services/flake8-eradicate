import subprocess

from flake8_eradicate import pkg_name, pkg_version


def test_call_flake8_version():
    """Checks that module is registered and visible in the meta data."""
    output = subprocess.check_output(
        ['flake8', '--version'],
        stderr=subprocess.STDOUT,
    )

    output_text = output.decode('utf-8')
    assert pkg_name in output_text
    assert pkg_version in output_text
