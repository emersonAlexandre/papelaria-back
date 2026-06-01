# Papelaria — Backend

API REST para gerenciamento de vendas e cálculo de comissões de vendedores, desenvolvida com **Python/Django** e **Django REST Framework**.

---

## Sumário

- [Visão geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e execução](#instalação-e-execução)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Estrutura do projeto](#estrutura-do-projeto)
- [API — Endpoints principais](#api--endpoints-principais)
- [Testes](#testes)
- [Decisões de arquitetura](#decisões-de-arquitetura)

---

## Visão geral

A API permite:

- **Cadastrar** produtos, clientes e vendedores (via Django Admin ou API REST).
- **Registrar vendas** com múltiplos itens (NF, data/hora, cliente, vendedor, produtos e quantidades).
- **Configurar regras de comissão por dia da semana** — percentuais mínimos e máximos que limitam a comissão do produto para vendas realizadas naquele dia.
- **Gerar relatórios de comissões** por período, exibindo o total a pagar para cada vendedor.

### Regra de cálculo de comissão

```
comissão_item = quantidade × valor_unitário × (percentual_efetivo / 100)
```

O `percentual_efetivo` é o percentual do produto **clampeado** pelo intervalo `[min, max]` da regra do dia da semana. Se não houver regra para o dia, usa-se o percentual original do produto.

**Exemplo:** segunda-feira com regra min=3% / max=5%
- Produto com comissão 10% → paga 5%
- Produto com comissão 2% → paga 3%
- Produto com comissão 4% → paga 4%

---

## Tecnologias

| Biblioteca | Versão | Função |
|---|---|---|
| Python | 3.11+ | Linguagem |
| Django | 4.2 | Framework web |
| Django REST Framework | 3.15 | API REST |
| django-filter | — | Filtros avançados nos endpoints |
| drf-spectacular | — | Documentação OpenAPI / Swagger |
| django-cors-headers | — | Controle de CORS |
| python-decouple | — | Configuração 12-factor via `.env` |
| pytest + pytest-django | — | Testes automatizados |

---

## Pré-requisitos

- **Python** 3.11+
- **pip**

---

## Instalação e execução

```bash
# 1. Criar e ativar virtualenv
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env
# edite .env se necessário (padrões funcionam para desenvolvimento)

# 4. Aplicar migrações
python manage.py migrate

# 5. Criar superusuário (para o Django Admin)
python manage.py createsuperuser

# 6. (Opcional) Carregar dados de demonstração
python manage.py seed_demo

# 7. Iniciar servidor de desenvolvimento
python manage.py runserver
```

Serviço disponível em: **http://localhost:8000**  
Admin: **http://localhost:8000/admin/**  
Swagger: **http://localhost:8000/api/docs/**

---

## Variáveis de ambiente

Copie `.env.example` para `.env` e ajuste conforme necessário:

| Variável | Padrão | Descrição |
|---|---|---|
| `SECRET_KEY` | `dev-secret-key-...` | Chave secreta do Django — **troque em produção** |
| `DEBUG` | `True` | Modo debug — usar `False` em produção |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Hosts permitidos (separados por vírgula) |
| `DB_NAME` | `db.sqlite3` | Nome do arquivo do banco SQLite |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000,...` | Origens permitidas pelo CORS |
| `CORS_ALLOW_ALL_ORIGINS` | `False` | Liberar CORS para todas as origens |

---

## Estrutura do projeto

```
backend/
├── papelaria/              # Configurações Django (settings, urls, wsgi)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── people/                 # App: Clientes e Vendedores
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests/
│       └── test_api.py
├── products/               # App: Produtos
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests/
│       └── test_api.py
├── sales/                  # App: Vendas e Itens de Venda
│   ├── models.py
│   ├── admin.py
│   ├── management/
│   │   └── commands/
│   │       └── seed_demo.py
│   └── tests/
│       └── test_api.py
├── commissions/            # App: Regras de comissão + relatório
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── services.py         # Lógica de negócio isolada (pura, sem Django)
│   └── tests/
│       ├── test_services.py
│       ├── test_api.py
│       └── test_rules.py
├── conftest.py             # Fixtures pytest compartilhadas
├── manage.py
├── requirements.txt
├── pytest.ini
└── .env.example
```

---

## API — Endpoints principais

| Método | Endpoint | Descrição |
|---|---|---|
| GET / POST | `/api/customers/` | Listar / criar clientes |
| GET / PUT / DELETE | `/api/customers/{id}/` | Detalhe / editar / excluir cliente |
| GET / POST | `/api/salespersons/` | Listar / criar vendedores |
| GET / PUT / DELETE | `/api/salespersons/{id}/` | Detalhe / editar / excluir vendedor |
| GET / POST | `/api/products/` | Listar / criar produtos |
| GET / PUT / DELETE | `/api/products/{id}/` | Detalhe / editar / excluir produto |
| GET / POST | `/api/sales/` | Listar / criar vendas |
| GET / PUT / DELETE | `/api/sales/{id}/` | Detalhe / editar / excluir venda |
| GET / POST | `/api/commission-rules/` | Listar / criar regras de comissão por dia |
| GET | `/api/commissions/report/` | Relatório de comissões por período |

### Parâmetros do relatório

```
GET /api/commissions/report/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```

### Filtros disponíveis nos endpoints de listagem

- **Paginação**: `?page=2`
- **Busca**: `?search=<termo>`
- **Ordenação**: `?ordering=name` ou `?ordering=-name`
- **Filtros**: `?customer=1`, `?sold_at_after=2024-01-01`

Documentação interativa (Swagger UI): `http://localhost:8000/api/docs/`

---

## Testes

```bash
# Rodar todos os testes
pytest

# Com relatório de cobertura
pytest --cov=. --cov-report=term-missing
```

### Cobertura dos testes

| Arquivo | O que testa |
|---|---|
| `commissions/tests/test_services.py` | Lógica de cálculo e clamping de comissão (unitários puros) |
| `commissions/tests/test_api.py` | Endpoint do relatório de comissões |
| `commissions/tests/test_rules.py` | CRUD de regras de comissão por dia |
| `sales/tests/test_api.py` | CRUD de vendas via API |
| `people/tests/test_api.py` | CRUD de clientes e vendedores |
| `products/tests/test_api.py` | CRUD de produtos |

---

## Decisões de arquitetura

### 12-Factor App

Todas as configurações sensíveis (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`) são lidas via `python-decouple` de variáveis de ambiente ou do arquivo `.env`, nunca hardcoded no código-fonte.

### Separação de responsabilidades (SOLID)

- **`commissions/services.py`**: lógica de cálculo de comissão completamente isolada do Django — sem ORM, sem views, sem dependências de framework. Facilita testes unitários puros e reuso.
- **Views**: responsáveis apenas por receber a requisição, delegar ao service e retornar a resposta.
- **Serializers**: responsáveis apenas por validação e serialização dos dados.

### Configuração do DRF

- Paginação global de 20 itens por página (`PageNumberPagination`).
- Filtros habilitados globalmente: `DjangoFilterBackend`, `SearchFilter`, `OrderingFilter`.
- Schema OpenAPI gerado automaticamente pelo `drf-spectacular`.
