CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id          VARCHAR PRIMARY KEY,
    source          VARCHAR NOT NULL,
    dataset         VARCHAR NOT NULL,
    operation       VARCHAR NOT NULL,
    started_at      TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at    TIMESTAMP WITH TIME ZONE,
    status          VARCHAR NOT NULL,
    rows_in         INTEGER DEFAULT 0,
    rows_out        INTEGER DEFAULT 0,
    rows_skipped    INTEGER DEFAULT 0,
    duration_seconds FLOAT,
    error_message   VARCHAR,
    parameters      VARCHAR
)
