from setuptools import setup, find_packages


setup(
    name='queue_mfc_manager',
    description='Simple queue manager for me and you!',
    author='Sergey Gavrilov',
    version='0.4.4',
    url='https://github.com/seregagavrilov/queue_mfc_manager',
    packages=find_packages(),
    include_package_data=True,
    author_email='sergeigavrilov123@gmail.com',
    py_modules=['workers', 'queue_manager', 'worker_helpers'],
    license='MIT',
    install_requires=[
        'Click == 6.7',
        'Redis == 2.10.6',
        'json-tricks == 3.11.3'
    ],
    entry_points='''
        [console_scripts]
        workers=workers:start_workers
        deletetasks=workers:delete_workers_from_queue
    ''',
)