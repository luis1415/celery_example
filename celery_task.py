from celery import Celery

app = Celery('tasks', broker='amqp://localhost//')

@app.task
def square(x):
    return x**2
