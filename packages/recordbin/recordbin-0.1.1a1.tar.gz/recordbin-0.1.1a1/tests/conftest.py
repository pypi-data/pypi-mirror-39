import pytest
from recordbin import RecordBin


@pytest.fixture
def URL():
    return "http://www.httpbin.com/post"


@pytest.fixture
def TOKEN():
    return "1234"


@pytest.fixture
def DATA():
    return {"username": "gtalarico"}


@pytest.fixture
def RESPONSE_DATA(DATA):
    return {"id": "456", "data": DATA}


@pytest.fixture
def bin(URL, TOKEN):
    return RecordBin(token=TOKEN, url=URL)
