CREATE TABLE IF NOT EXISTS File (
    name    TEXT NOT NULL PRIMARY KEY,
    ext     TEXT NOT NULL,
    size    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Experiment (
    file            TEXT NOT NULL,
    version         TEXT NOT NULL,
    bucket          TEXT NOT NULL,
    cluster         TEXT NOT NULL,
    node            TEXT NOT NULL,
    tool            TEXT NOT NULL,
    file_split_size TEXT NOT NULL,
    segment_size    TEXT NOT NULL,
    thread          INTEGER,
    core            INTEGER,
    process         INTEGER,
    transfer_rate   TEXT,
    transfer_time   TEXT NOT NULL,

    FOREIGN KEY (file) REFERENCES File(name)
);

