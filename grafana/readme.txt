A pasta provisioning está dividida em duas diretorias: dashboard e datasource.

dashboard:
Diretoria onde estão localizados os ficheiros .json dos gráficos do Grafana. Estes ficheiros são exportados no Grafana sempre que houver
alterações nos respetivos gráficos. No Grafana, após a alteração de algo num gráfico, carregar em "Apply" e depois "Save" para exportar
o ficheiro .json.
Dentro desta pasta existe também um ficheiro .yml que corresponde à configuração dos gráficos no Grafana.

datasource:
Ficheiro .yml de configuração da base de dados onde o Grafana acede para a visualização dos dados.