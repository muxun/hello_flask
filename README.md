# hello_flask
test task about docker,ansible and flask
<h2>Описание</h2>

Насколько я понял задание, цель - показать как с помощью ansible развернуть многосервисное приложение в docker контейнерах на удаленном хосте.

Основная проблема, с которой столкнулся при выполнении задания - построение веб-сервисов.
Пока я не смог решить проблему, как можно запросить данные одним приложением от другого, и получив их (данные), отобразить в браузере.
Между тем, используемая связка docker-compose для контейнеров router и hello отрабатывает, контейнеры видят друг друга по алиасам сети.
Вот например, скрин, на котором  из контейнера router к контейнеру hello произведен get запрос '/'  и получен ответ Hello World!
<img src="https://raw.githubusercontent.com/muxun/muxun.github.io/master/getrouterhello.png"></img>

Для боевого сервиса я захардкодил ip адрес удаленного хоста в код приложения router, 
таким образом, что при обращении к /hello мой router перенаправляет запрос  на ip адрес хоста по порту 5000, 
тем самым, подключается к приложению hello. Понимаю, что данное решение - костыль,но пока так.

<h2>Что сделано</h2>

* на удаленном сервере с помощью visudo прописан парметр NOPASSWD: ALL для группы sudo
* написаны два Flask приложения router и hello 
* для данных приложений созданы Dockerfile. 
При написании dockerfile старался уменьшить размеры создаваемых слоев при помощи пайпов в командах RUN
* образы собраны на моей машине и отправлены в личный докер-хаб
* написал docker-compose файл (лежит в роли  deploy_docker/files)
* созданы ansible роли:
  - ansible_prerequisites - сюда вынес установку python и модулей для корректной работы ansible. Я тестировал на GCP платформе на чистых инстансах, так что добавлял модули по мере возникновения ошибок
  - install_docker - установка docker engine и docker-compose по мануалу из официальной документации
  - deploy_docker - копирование docker-compose и запуск сервисов

При написании тасков ansible старался максимально использовать ansible модули. Но,например, на вашем сервере модули pip отказались работать, хотя на тестовой машине исполнялись. В итоге pip модуль в ansible поменял на command

<h2>Как проверить</h2>

перейти по адресу 

```
http://95.216.170.95:4000/

```
Вас встретит приложение router и попросит ввести /hello после ip:port

```
http://95.216.170.95:4000/hello
```

router перенаправит запрос в приложение hello , которое ответит Hello World

<h2>summary</h2>
* затрачено времени на всю работу с тестированием и ловлей багов  ~ 28 часов  

<details><summary>Листинг работы плэйбука</summary>
```
~/projects/hello_flask/ansible [master ↑·2|✔] 
22:28 # ansible-playbook install_and_deploy.yml 

PLAY [Install and deploy microservices flask app] **********************************************************************************************************************

TASK [ansible_prerequisites : Install python] **************************************************************************************************************************
changed: [95.216.170.95]

TASK [ansible_prerequisites : Install pip] *****************************************************************************************************************************
changed: [95.216.170.95]

TASK [ansible_prerequisites : Install ssl backports module] ************************************************************************************************************
ok: [95.216.170.95]

TASK [ansible_prerequisites : Install setuptools module] ***************************************************************************************************************
changed: [95.216.170.95]

TASK [ansible_prerequisites : Install docker pip  module] **************************************************************************************************************
changed: [95.216.170.95]

TASK [ansible_prerequisites : Install dokcer-compose pip module] *******************************************************************************************************
changed: [95.216.170.95]

TASK [install_docker : Add Docker gpg key] *****************************************************************************************************************************
ok: [95.216.170.95]

TASK [install_docker : Add docker repository] **************************************************************************************************************************
ok: [95.216.170.95]

TASK [install_docker : Install misc packages for docker] ***************************************************************************************************************
[DEPRECATION WARNING]: Invoking "apt" only once while using a loop via squash_actions is deprecated. Instead of using a loop to supply multiple items and specifying 
`name: "{{ item }}"`, please use `name: ['aptitude', 'apt-transport-https', 'ca-certificates', 'curl', 'software-properties-common']` and remove the loop. This feature
 will be removed in version 2.11. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
ok: [95.216.170.95] => (item=[u'aptitude', u'apt-transport-https', u'ca-certificates', u'curl', u'software-properties-common'])

TASK [install_docker : Install docker-ce] ******************************************************************************************************************************
ok: [95.216.170.95]

TASK [install_docker : Install docker-compose] *************************************************************************************************************************
 [WARNING]: Consider using the get_url or uri module rather than running curl.  If you need to use command because get_url or uri is insufficient you can add
warn=False to this command task or set command_warnings=False in ansible.cfg to get rid of this message.

changed: [95.216.170.95]

TASK [install_docker : Make docker-compose executable] *****************************************************************************************************************
ok: [95.216.170.95]

TASK [deploy_docker : Copy docker-compose.yml file] ********************************************************************************************************************
changed: [95.216.170.95]

TASK [deploy_docker : Run services from docker-compose.yml] ************************************************************************************************************
changed: [95.216.170.95]

PLAY RECAP *************************************************************************************************************************************************************
95.216.170.95              : ok=14   changed=8    unreachable=0    failed=0

```
</details>

   
