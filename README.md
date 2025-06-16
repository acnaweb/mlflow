
# MLflow + Docker Compose Example

## 📂 Estrutura de Pastas

```sh
mlflow/
├── .dockerignore
├── .flake8
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── Makefile
├── README.md
├── compose.yaml
├── metadata.json
├── mypy.ini
├── pyproject.toml
├── requirements.dev.txt
├── requirements.quality.txt
├── requirements.txt
└── src/
```

## ✅ Explicação dos Componentes

| Arquivo/Pasta | Função |
|---|---|
| `Dockerfile` | Cria a imagem Docker para o serviço `mlflow`, incluindo instalação de dependências |
| `compose.yaml` | Define os serviços Docker (Postgres, MinIO, criação de bucket e MLflow Server) |
| `Makefile` | Comandos de automação para build, up, down e testes |
| `requirements.txt` | Dependências principais do projeto |
| `requirements.dev.txt` | Dependências para desenvolvimento (ex: pytest, flake8) |
| `requirements.quality.txt` | Dependências para ferramentas de qualidade de código (ex: mypy, isort) |
| `.pre-commit-config.yaml` | Configura pre-commit hooks para linting e validação de código antes de commits |
| `.flake8`, `mypy.ini` | Configurações de qualidade de código (style, type checking) |
| `.dockerignore`, `.gitignore` | Arquivos e pastas que serão ignorados em builds e no Git |
| `metadata.json` | Metadados possivelmente usados por CI/CD ou MLflow |
| `src/` | Código-fonte Python principal (exemplo: scripts de experimentos ML) |

## ✅ Serviços Docker no `compose.yaml`

| Serviço | Imagem | Descrição |
|---|---|---|
| `database` | `postgres` | Armazena o backend do MLflow (tracking data) |
| `minio` | `quay.io/minio/minio` | Simula um S3 para armazenar artifacts do MLflow |
| `create-bucket` | `minio/mc` | Container temporário que cria o bucket `mlflow` dentro do MinIO |
| `mlflow` | Build local via `Dockerfile` | Roda o MLflow Tracking Server com backend em Postgres e artifacts no MinIO |

## ✅ Instruções de Uso

### 1. Construir o ambiente:

```bash
docker compose build
```

### 2. Subir os serviços:

```bash
docker compose up
```

### 3. Acessar os serviços:

| Serviço | URL |
|---|---|
| MLflow UI | [http://localhost:5000](http://localhost:5000) |
| MinIO Console | [http://localhost:9001](http://localhost:9001) |
| Postgres | localhost:5432 (user: `mlflow`, senha: `mlflow`) |

### 4. Variáveis de Ambiente (para o Client MLflow)

Se quiser rodar experimentos locais:

```bash
export MLFLOW_TRACKING_URI=http://localhost:5000
export AWS_ACCESS_KEY_ID=minio
export AWS_SECRET_ACCESS_KEY=minio_pwd
export MLFLOW_S3_ENDPOINT_URL=http://localhost:9000
```

### 5. Exemplo de script Python para conectar:

```python
import os
import mlflow

os.environ["AWS_ACCESS_KEY_ID"] = "minio"
os.environ["AWS_SECRET_ACCESS_KEY"] = "minio_pwd"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("meu_experimento")

with mlflow.start_run():
    mlflow.log_param("param1", 5)
    mlflow.log_metric("accuracy", 0.95)
```

### 6. Outros comandos úteis:

| Comando | Função |
|---|---|
| `docker compose down -v` | Derrubar todos os containers e apagar os volumes (útil pra resetar o estado) |
| `make quality` | Rodar linters e type-checkers |
| `make tests` | Executar os testes unitários (se houver) |