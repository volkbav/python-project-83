CREATE TABLE IF NOT EXISTS urls (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP
);
CREATE TABLE IF NOT EXISTS url_checks (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    url_id BIGINT
        REFERENCES urls(id),
    status_code BIGINT,
    h1 TEXT,
    title TEXT,
    description TEXT,
    created_at TIMESTAMP
);