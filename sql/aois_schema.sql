CREATE TABLE IF NOT EXISTS incidents (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    raw_log TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('P1', 'P2', 'P3', 'P4')),
    status TEXT NOT NULL DEFAULT 'open',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analyses (
    id BIGSERIAL PRIMARY KEY,
    incident_id BIGINT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    summary TEXT NOT NULL,
    suggestion TEXT NOT NULL,
    analyzer TEXT NOT NULL,
    confidence NUMERIC(4,3),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS incidents_created_at_idx ON incidents (created_at DESC);
CREATE INDEX IF NOT EXISTS incidents_severity_idx ON incidents (severity);
CREATE INDEX IF NOT EXISTS analyses_incident_id_idx ON analyses (incident_id);
