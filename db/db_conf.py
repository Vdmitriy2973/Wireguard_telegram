import dataclasses


@dataclasses.dataclass
class DataBaseSettings:
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url_psycopg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

db_settings = DataBaseSettings("localhost", 5432, "postgres", "*&bvn8(Y^23-bhBV8_", "wireguard_db")