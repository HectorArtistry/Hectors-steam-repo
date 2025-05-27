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
│ ├── csv_file_layout.md
│ └── flowchart.md

├── etl/
│ ├── extract/ # (API) data already extracted and loaded into data/raw
│ ├── load/
│ │ └── load.py # database inserts + lookup helpers
│ ├── SQL/
│ │ └── steam_schema.sql # Database SQL schema
│ └── transform/
│   └── transform.py # Transformation.py is now empty, due to requirements of transformation within load.py

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
│ ├── run_tests.py
│ └── test.py

├── utils/
│ └── logging_utils.py

├── .env.dev
├── .env.test
├── .flake8
├── .gitignore
├── .sqlfluff
├── README.md
└── requirements.txt