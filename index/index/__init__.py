"""Initialize index."""
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name
import index.api  # noqa: E402  pylint: disable=wrong-import-position
# INIT:
# FIrst time page called on flask oNCE
# CALL funcitons here  to do stuff
# import index.api
# index.apie.file.func
