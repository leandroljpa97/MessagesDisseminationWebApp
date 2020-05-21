# MessagesDisseminationWebApp

Construção de uma aplicação WEB que tem como objetivo aos alunos do IST (restrito a alunos do IST pois é necessário autenticar com o sistema de autenticação do IST) que permite detetar através das coordenadas geográficas em que edifício do Técnico a pessoa se encontra e permite ver todas as pessoas que se encontram nesse edifício e enviar mensagem e receber por parte dessas pessoas em tempo real. Permite definir um range e enviar mensagens e receber para pessoas que se encontram dentro desse range.
Ferramentas utilizadas: Django para a REST API, JavaScript, HTML, CSS para a interface do utilizador

Nota: 19/20
Relatório em:


# Execução
run locally:

	start the data base instance locally, listenning on port 3306,

	$ ./cloud_sql_proxy -instances="asint-227820:europe-west1:sqlinstance"=tcp:3306

	launch the Django app locally,

	$ python manage.py runserver

access locally:

	- type 127.0.0.1:8000/app/ as a browser client.

deploy the app in the remote google cloud app engine:

	$ gcloud app deploy

access remotly:

	- type https://asint-227820.appspot.com/app/ as a browser client.
