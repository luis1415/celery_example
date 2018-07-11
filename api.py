from flask import Flask, request
from celery import Celery
import json


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='amqp://localhost//',
    CELERY_RESULT_BACKEND='mongodb://localhost:27017//celery'
)
celery = make_celery(app)

@celery.task()
def add_together(a, b):
    return a + b

@app.route("/process", methods=['GET'])
def process():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    return json.dumps({'suma': a + b})

if __name__ == '__main__':
    app.run(debug=True)
