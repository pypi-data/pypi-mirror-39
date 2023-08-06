========
handlers
========

Handlers is a simple Django app to write logs into databases. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "handlers" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'SenseCore.handlers',
    ]

2. Config your handlers under LOGGING settings like this::
	
	LOGGING = {
		...
		'handlers':{
			'lever':'',
			'class':'SenseCore.handlers.handlers.DatabaseHandler',
			...
		}
	}
	
https://www.xncoding.com/2017/05/26/mq/rabbitmq-tutorial08.html
	
docker run -d --hostname sd-rabbit --name rabbit -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=sense@2018 -p 15672:15672 -p 5672:5672 -p 25672:25672 -p 61613:61613 -p 1883:1883 rabbitmq:management
