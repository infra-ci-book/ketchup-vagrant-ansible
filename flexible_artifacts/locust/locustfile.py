from locust import HttpLocust, TaskSet, task

class KetchupTasks(TaskSet):

    @task
    def admin(self):
        self.client.get("/admin/login")

class WebsiteUser(HttpLocust):
    task_set = KetchupTasks
    min_wait = 500
    max_wait = 1000
