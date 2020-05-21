# MessagesDisseminationWebApp

Construção de uma aplicação WEB que tem como objetivo aos alunos do IST (restrito a alunos do IST pois é necessário autenticar com o sistema de autenticação do IST) que permite detetar através das coordenadas geográficas em que edifício do Técnico a pessoa se encontra (se é no pavilhão de engenharia civíl, no pavilhão central) e permite ver todas as pessoas que se encontram nesse edifício e enviar mensagem e receber por parte dessas pessoas em tempo real. Permite definir um range e enviar mensagens e receber para pessoas que se encontram dentro desse range.
Permite também a um administrador (um funcionário de uma sala de estudo) utilizar a aplicação e criar um bot, para enviar avisos automaticamente todos os dias a dizer que a sala de estudo fecha daqui a 10 mins por exemplo, a todos os alunos que se encontram no seu interior.
Basicamente, o cliente envia pedidos POST com as coordenadas, e o servidor deteta em que edificio está e armazena essa informação numa base de dados.
Há Autenticação com o sistema FENIX, ou seja só quem tem conta no fénix pode aceder.

Ferramentas utilizadas: Django para a REST API, JavaScript, HTML, CSS para a interface do utilizador

Nota: 19/20

Relatório em: Asint_Report (1).pdf


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
