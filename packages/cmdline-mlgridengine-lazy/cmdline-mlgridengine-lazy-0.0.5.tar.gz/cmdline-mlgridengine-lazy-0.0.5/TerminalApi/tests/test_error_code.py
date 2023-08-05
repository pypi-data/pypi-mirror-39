from src.error_codes.error_codes import handle_error


def test_error_code():
    assert handle_error(200) is None
    assert handle_error(400) is None
    assert handle_error(400, list_files=True) is None
    assert handle_error(400, retrieve=True) is None
    assert handle_error(401) is None
    assert handle_error(403) is None
    assert handle_error(404) is None
    assert handle_error(404, realtime=True) is None
    assert handle_error(405) is None
    assert handle_error(409, launch_task=True) is None
    assert handle_error(413) is None
    assert handle_error(500) is None
    assert handle_error(501) is None
    assert handle_error(503) is None
    assert handle_error(507) is None
    assert handle_error(409, retrieve=True) is None
    assert handle_error(409, realtime=True) is None
    assert handle_error(409, download_file=True) is None
    assert handle_error(409) is None
