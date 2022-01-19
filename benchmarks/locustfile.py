from locust import HttpUser, task


_ids = []
with open('.fixtures/input-3.json', 'r') as f:
    import json
    file = json.load(f)
for vm in file['vms']:
    _ids.append(vm['vm_id'])


class HelloWorldUser(HttpUser):

    @task(6)
    def hello_world(self):
        for vm_id in _ids:
            self.client.get("/api/v1/attack/?vm_id=" + vm_id)

    @task(1)
    def hello_stats(self):
        self.client.get("/api/v1/stats/")
        # for i in range(len(self._ids)):
        #     self.client.get("/api/v1/attack/?vm_id=vm-11111" + str(i))
