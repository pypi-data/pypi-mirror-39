from setuptools import setup, find_packages

# with open('demo_project_test_time/requirements.txt') as f:
#     required = f.read().splitlines()

setup(
    name="app_music",
    version="0.003",
    packages=find_packages(),
    py_modules=["API", "server", "app", "config", "database", "docs", "mq", "rec", "server", "utils"],
    include_package_data=True,
    platforms="any",
    install_requires=["numpy",
                      "pandas",
                      "tornado",
                      "redis",
                      "sqlalchemy",
                      "kazoo",
                      "pika",
                      "ruamel.yaml",
                      "requests",
                      "pymysql"
                      ],
    # data_files=[('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
    # ('config', ['cfg/data.cfg']), ('/etc/init.d', ['init-script'])]
    data_files=[('config', ['app_music/config/app_music.conf'])]
)
