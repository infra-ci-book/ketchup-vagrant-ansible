from locust import HttpLocust, TaskSet, task

class KetchupTasks(TaskSet):
    @task
    def login(self):
        self.client.get("/admin/login")

    @task
    def ping(self):
        self.client.get("/ping")

class WebsiteUser(HttpLocust):
    task_set = KetchupTasks
    min_wait = 500
    max_wait = 1500
