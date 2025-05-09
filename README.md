## 📦 Universal MLOps Platform: Automated Deployment with Apache Spark, Airflow, Prometheus and Grafana

### 📖 Описание

Этот проект предоставляет *готовую к использованию MLOps-платформу*, разворачиваемую локально с помощью **Ansible** и **Docker Compose**. Она включает в себя:

* **Apache Airflow** для оркестрации DAG-пайплайнов
* **Apache Spark** (master + worker) для обработки данных
* **PostgreSQL** для хранения метаданных Airflow
* **Redis** как брокер задач
* **Prometheus + Grafana** для мониторинга состояния
* **Airflow Exporter** для сбора метрик из Airflow API

---

## 🗂️ Структура проекта

```
your-project/
├── ansible/
│   ├── airflow/               # Dockerfile и DAG-файлы Airflow
│   │   ├── dags/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── monitoring/            # Airflow Exporter + конфиги Prometheus
│   │   ├── airflow-exporter/
│   │   │   ├── Dockerfile
│   │   │   ├── requirements.txt
│   │   │   └── airflow_exporter.py
│   │   └── prometheus.yml
│   ├── spark/
│   │   └── spark-defaults.conf
│   ├── shared/
│   │   └── jars/
│   ├── docker-compose.yml     # Docker Compose-файл
│   ├── inventories/
│   │   └── production.yml     # Ansible inventory
│   ├── playbook.yml           # Основной Ansible playbook
│   └── roles/
│       └── deploy/
│           ├── tasks/
│           │   └── main.yml   # Логика развертывания
│           └── files/         # Сюда копируются все вышеуказанные файлы
```

---

## 🚀 Быстрый запуск

### 1. Установите зависимости

```bash
sudo apt update
sudo apt install ansible docker.io docker-compose-plugin -y
ansible-galaxy collection install community.docker
ansible-galaxy collection install ansible.posix
```

### 2. Разверните всё

Из корня проекта `your-project/`:

```bash
cd ansible
ansible-playbook -i inventories/production.yml playbook.yml
```

### 3. Доступ к сервисам

| Сервис          | URL                                              | Комментарий                |
| --------------- | ------------------------------------------------ | -------------------------- |
| Airflow         | [http://localhost:28080](http://localhost:28080) | `admin/admin`              |
| Spark Master UI | [http://localhost:18080](http://localhost:18080) |                            |
| Spark Worker UI | [http://localhost:18081](http://localhost:18081) |                            |
| Prometheus      | [http://localhost:19001](http://localhost:19001) |                            |
| Grafana         | [http://localhost:3000](http://localhost:3000)   | `admin/admin` по умолчанию |

---

## 🛠️ Конфигурация

* Все DAG-файлы находятся в `ansible/airflow/dags/`
* Конфигурация Spark — `ansible/spark/spark-defaults.conf`
* Метрики настраиваются через `ansible/monitoring/prometheus.yml`
* Airflow Exporter использует API `/api/v1/dags`, `/health` и `/metrics`

---

## 📦 Как перенести на другую машину

1. Скопируйте всю папку `your-project/` как есть
2. Установите зависимости (см. выше)
3. Выполните `ansible-playbook`, как указано выше
4. Всё будет развернуто в автономном режиме без необходимости ручной настройки

---

## 📚 Примечания

* `docker-compose.yml` размещён в `ansible/`, чтобы все пути были локальными
* Контейнеры собираются с нуля при первом запуске, включая установку зависимостей через `requirements.txt`
* В будущем возможно расширение: подключение MinIO, MLflow, S3 или CI/CD пайплайнов
* В случае возникновения конфликтов с Ansible, установите новейшую стабильную версию напрямую из их Github
