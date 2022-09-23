Correr o docker-compose para iniciar os containers.


Dashboard -> localhost:8000
API -> localhost:80
Phpmyadmin -> localhost:8080
Grafana -> localhost:3000
Porto para comunicar com a framework -> 9999

Para ver os gráficos no Grafana, no ícone da lupa, ir para "Search Dashboards" e escolher o dashboard "All Measurements". Se enviar uma métrica diferente (ex. altura da água), terá que mudar a variável global "metric_name" para o nome da variável, tal como é inserida na base de dados. Para mudar está em cima do gráfico.

Exemplo de mensagem esperada pelo servidor: {"time": 1627776922000, "value": 94, "type": "height", "sensor": "lnec"}