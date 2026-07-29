CREATE TABLE metrics (

    id NUMBER GENERATED ALWAYS AS IDENTITY,

    metric_id NUMBER,

    metric_name VARCHAR2(200),

    abbreviation VARCHAR2(50),

    sheet_name VARCHAR2(200),

    source_workbook VARCHAR2(200),

    row_number NUMBER,

    period VARCHAR2(20),

    value NUMBER,

    unit VARCHAR2(20),

    category VARCHAR2(100),

    CONSTRAINT metrics_pk PRIMARY KEY(id)

);