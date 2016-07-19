import logging
import sys
from .app import create_app
from z_logging_formatters import JSONLoggingFormatter

# Entry point for staring the dev server without debug mode.
def main():
    app.run(
        host='0.0.0.0',
        port=5000
    )

# flask requires setting up logging ourselves.
# we log to stdout so this is picked up via apache.
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(JSONLoggingFormatter())
out_hdlr.setLevel(logging.INFO)
logging.getLogger().addHandler(out_hdlr)

app = create_app('config.yaml')
# Must use app.logger.setLevel so the level takes effect when running via apache.
app.logger.setLevel(logging.INFO)
