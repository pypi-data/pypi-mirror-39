env_conf = [
    {
        "env": "dev-debug",
        "url": "http://172.16.101.169:9090"
    },
    {
        "env": "dev-fulltime",
        "url": "http://172.16.101.166:9090"
    },
    {
        "env": "dev-guanhua",
        "url": "http://172.16.101.138:9090"
    },
    {
        "env": "test1",
        "url": "http://172.16.101.50:9090"
    },
    {
        "env": "test7",
        "url": "http://172.16.101.131:9090"
    },
    {
        "env": "test8",
        "url": "http://172.16.101.76:9090"
    },
{
        "env": "test-pay",
        "url": "http://172.30.1.244:9090"
    },
    {
        "env": "staging",
        "url": "http://172.31.2.179:8181"
    },
    {
        "env": "prod",
        "url": "http://172.20.12.241:9090"
    }
]


def get_available_env():
    envs = map(lambda x: x.get('env'), env_conf)
    envs.sort(key=lambda x: x)
    return ', '.join(envs)
