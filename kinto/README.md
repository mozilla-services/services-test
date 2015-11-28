###Run API tests###

From /kinto/

1. virtualenv .
2. ./bin/pip install -r dev-requirements.txt
3. ./bin/nosetest -w api-test/
