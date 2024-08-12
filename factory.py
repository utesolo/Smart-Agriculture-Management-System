from flask import Flask
from flask_apscheduler import APScheduler


scheduler = APScheduler()


def create_app():
    app = Flask(__name__)
    app.secret_key = '09hxb2PXq31UstkTWtWK3qt136hBoDdbKwOj3Too'  # 随机生成，可以在util的aksk生成器中生成
    app.config.update(
        {
            "SCHEDULER_API_ENABLED": True,
            "JOBS":[{"id":"job_function",
                     "func":"task:job_function",
                     "args":(),
                     "trigger":"interval",
                     "hours":1,}],
        }
    )
    scheduler.init_app(app)
    scheduler.start()
    return app
