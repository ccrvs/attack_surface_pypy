from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._ids = []
        with open('./input-3.json', 'r') as f:
            import json
            file = json.load(f)
        for vm in file['vms']:
            self._ids.append(vm['vm_id'])

    @task
    def hello_world(self):
        for vm_id in self._ids:
            self.client.get("/api/v1/attack/?vm_id=" + vm_id)
        for i in range(len(self._ids)):
            self.client.get("/api/v1/attack/?vm_id=vm-11111" + str(i))
