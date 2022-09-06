import ray, os

@ray.remote
def e():
    return ["bruh"]

def run():
    ray.init()
    f = ray.get([e.remote() for i in range(os.cpu_count())])
    print(f)

run()