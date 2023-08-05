import pytest  # noqa
import responses
import requests


@responses.activate
def test_post(bin, DATA, RESPONSE_DATA, URL):
    responses.add(
        responses.POST, f"{URL}/api/v1/records/", status=201, json=RESPONSE_DATA
    )
    resp = bin.post(DATA).result()
    assert resp.status_code == 201
    assert resp.json() == RESPONSE_DATA


@responses.activate
def test_auth_header(bin, DATA, RESPONSE_DATA, TOKEN, URL):
    responses.add(responses.POST, f"{URL}/api/v1/records/", status=201)
    resp = bin.post(DATA).result()
    auth_header = resp.request.headers["Authorization"]
    assert auth_header == f"AppToken {TOKEN}"


@responses.activate
def test_invalid(bin, DATA, RESPONSE_DATA, TOKEN, URL):
    responses.add(responses.POST, f"{URL}/api/v1/records/", status=401)
    with pytest.raises(requests.exceptions.HTTPError):
        bin.post(DATA).result()


@responses.activate
def test_futures(bin, URL, DATA, RESPONSE_DATA):
    responses.add(
        responses.POST, f"{URL}/api/v1/records/", json=RESPONSE_DATA, status=201
    )
    future = bin.post(DATA)
    assert hasattr(future, "done")
    assert future.result().json() == RESPONSE_DATA


def test_versions():
    from recordbin import __version__  # noqa
