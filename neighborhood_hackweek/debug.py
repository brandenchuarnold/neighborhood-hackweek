from .app import create_app


# Entry point for starting the dev server in debug mode
def debug():
    app.run(
        host='0.0.0.0',
        port=5000
    )


app = create_app('config.yaml')
app.debug = True
