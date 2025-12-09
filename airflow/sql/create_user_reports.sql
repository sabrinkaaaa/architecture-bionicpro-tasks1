CREATE TABLE IF NOT EXISTS user_reports
(
    user_id UInt64,
    report_date Date,
    avg_response_ms Float64,
    total_events UInt32,
    telemetry_json String,
    crm_json String
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(report_date)
ORDER BY (user_id, report_date);
