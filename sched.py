from apscheduler.schedulers.background import BackgroundScheduler
import redis_helper

sched = BackgroundScheduler(timezone='Asia/Seoul')
PROC = {}



def task_data_reset():
  print("reset task DB")
  redis_helper.reset_task_db()


def start():
  sched.add_job(task_data_reset, trigger='cron', day_of_week='2', hour='5', minute='0')
  sched.start()
