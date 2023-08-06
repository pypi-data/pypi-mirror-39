from fdnutil import Connection
import re

def test_dsn_converter():
    DSN = 'postgresql://postgres:secret@localhost/speech_analysis'
    conn = Connection(DSN)
    assert conn.db == 'speech_analysis'
    assert conn.host == 'localhost'
    assert conn.username == 'postgres'
    assert conn.password == 'secret'

def test_regex():
    rx = re.compile(r"([\w]+)")
    m = rx.match("hello")
    assert m.group(0) == 'hello'