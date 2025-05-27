Hectors Steam Repo/
├── .venv/ # Virtual environment

├── config/
│ ├── db_config.py
│ └── env_config.py

├── data/
│ ├── api_pulled_data/ # To be left empty
│ ├── processed/
│ ├── raw/ # Raw CSVs are here
│ └── steam_data.db
├── docs/
│ └── flowchart/

├── etl/
│ ├── extract/ # (API) data already extracted and loaded into data/raw
│ ├── load/
│ │ └── load.py # database inserts + lookup helpers
│ ├── SQL/
│ │ └── steam_schema.sql # Database SQL schema
│ └── transform/
│ └── transform.py # Transformation logic

├── scripts/
│ └── run_etl.py # Pipeline execution

├── streamlit_app/
│ ├── assets/
│ ├── pages/
│ └── app.py

├── tests/
│ ├── component_tests/
│ │ └── .gitkeep
│ ├── integration_tests/
│ │ └── .gitkeep
│ ├── unit_tests/
│ │ └── test_db_config.py
│ └── run_tests.py

├── utils/
│ └── logging_utils.py

├── .coveragerc
├── .env.dev
├── .env.test
├── .flake8
├── .gitignore
├── .sqlfluff
├── README.md
└── requirements.txt