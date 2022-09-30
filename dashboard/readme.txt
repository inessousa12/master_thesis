Diretoria relacionada com o dashboard. O ficheiro principal é o index.php. Está dividida em 4 pastas: css, img, js e php_includes.

css:
Diretoria onde se encontra o ficheiro .css.

img:
Diretoria onde se encontram todas as imagens utilizadas no dashboard.

js:
Diretoria onde se encontram os ficheiros .js utilizados pelo dashboard.
    -> bd_functions.js - ficheiro onde é tratado todas as interações com a base de dados. Ex: adicionar uma estação,
                         editar uma estação, apagar uma estação, etc.
    -> map.js - ficheiro onde tudo o que é relacionado com o mapa no dashboard é tratado. Utiliza a API do HereWeGo.
    -> measurement_graphs.js - ficheiro que mostra os gráficos a mostrar quando uma métrica é selecionada na sidebar.
    -> sidebar_slide.js - ficheiro que anima a sidebar.
    -> sidebar.js - ficheiro onde todas as ações realizadas na sidebar são tratadas. É aqui onde as ações do modal
                    CONFIG são realizadas.

php_includes:
Diretoria que consiste em ficheiros que são usados pelo index.php e em ficheiros que comunicam com a base de dados.
Ficheiros que acabem em "_page.php" são ficheiros com código HTML. Os restantes comunicam com a base de dados.