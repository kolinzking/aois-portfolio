-- Phase 0 v0.8 AOIS portfolio persistence foundation.
-- This file is Postgres-oriented DDL, but the lesson does not require
-- starting Postgres on the shared server.
--
-- Server-visible namespace rule:
-- use aois_p for portfolio database objects so they cannot be confused with
-- the primary AOIS project.

CREATE SCHEMA IF NOT EXISTS aois_p;

CREATE TABLE IF NOT EXISTS aois_p.incidents (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL DEFAULT 'manual',
    message TEXT NOT NULL CHECK (length(trim(message)) > 0),
    status TEXT NOT NULL DEFAULT 'new'
        CHECK (status IN ('new', 'analyzed', 'archived')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_aois_p_incidents_created_at
    ON aois_p.incidents (created_at DESC);

CREATE INDEX IF NOT EXISTS idx_aois_p_incidents_status
    ON aois_p.incidents (status);

CREATE TABLE IF NOT EXISTS aois_p.analysis_results (
    id BIGSERIAL PRIMARY KEY,
    incident_id BIGINT NOT NULL REFERENCES aois_p.incidents(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'unknown')),
    confidence NUMERIC(4, 3) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    summary TEXT NOT NULL CHECK (length(trim(summary)) > 0),
    recommended_action TEXT NOT NULL CHECK (length(trim(recommended_action)) > 0),
    analyzer_version TEXT NOT NULL DEFAULT 'phase0-deterministic',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_aois_p_analysis_results_incident_id
    ON aois_p.analysis_results (incident_id);

CREATE TABLE IF NOT EXISTS aois_p.llm_request_plans (
    id BIGSERIAL PRIMARY KEY,
    incident_id BIGINT REFERENCES aois_p.incidents(id) ON DELETE SET NULL,
    model TEXT NOT NULL DEFAULT 'provider-model-placeholder',
    response_format TEXT NOT NULL DEFAULT 'json_object'
        CHECK (response_format IN ('json_object', 'text')),
    system_prompt TEXT NOT NULL CHECK (length(trim(system_prompt)) > 0),
    user_prompt TEXT NOT NULL CHECK (length(trim(user_prompt)) > 0),
    temperature NUMERIC(3, 2) NOT NULL DEFAULT 0 CHECK (temperature >= 0 AND temperature <= 2),
    max_output_tokens INTEGER NOT NULL CHECK (max_output_tokens > 0),
    estimated_total_tokens INTEGER NOT NULL CHECK (estimated_total_tokens > 0),
    estimated_cost_usd NUMERIC(12, 6) NOT NULL CHECK (estimated_cost_usd >= 0),
    latency_budget_ms INTEGER NOT NULL CHECK (latency_budget_ms > 0),
    provider_call_allowed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_aois_p_llm_request_plans_incident_id
    ON aois_p.llm_request_plans (incident_id);

-- Practice inserts for reading only unless a database run has been approved.
-- INSERT INTO aois_p.incidents (source, message)
-- VALUES ('lab', 'gateway returned 5xx after deploy');
--
-- SELECT id, source, status, created_at
-- FROM aois_p.incidents
-- ORDER BY created_at DESC
-- LIMIT 5;
