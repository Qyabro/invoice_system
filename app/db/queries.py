GET_INVOICE_QUERY = """
WITH data AS (
    SELECT records.record_timestamp, 
           injection.value AS hourly_injection,
           SUM(injection.value) OVER (ORDER BY records.record_timestamp) AS cumulative_injection,
           SUM(consumption.value) OVER () AS total_consumption,
           xm_data_hourly_per_agent.value AS invoice_factor
    FROM records
    JOIN injection ON records.id_record = injection.id_record
    JOIN consumption ON records.id_record = consumption.id_record
    JOIN xm_data_hourly_per_agent ON records.record_timestamp = xm_data_hourly_per_agent.record_timestamp    
    WHERE records.id_service = $1  
      AND records.record_timestamp >= $2
      AND records.record_timestamp < $3
),
ee_calculated AS (
    SELECT CASE 
               WHEN cumulative_injection <= total_consumption THEN 0
               WHEN cumulative_injection > total_consumption AND 
                    MIN(cumulative_injection) FILTER (WHERE cumulative_injection > total_consumption) 
                    OVER () = cumulative_injection 
               THEN (cumulative_injection - total_consumption) * invoice_factor
               ELSE hourly_injection * invoice_factor
           END AS ee2
    FROM data
),
total_ee AS (
    SELECT SUM(ee2) AS total_ee2 FROM ee_calculated
)
SELECT records.id_service,        
       services.id_market, services.cdi, services.voltage_level,       
       SUM(consumption.value) AS total_consumption,
       SUM(injection.value) AS total_injection,
       tariffs.cu, tariffs.c,
       SUM(consumption.value) * tariffs.CU AS ea,
       SUM(injection.value) * tariffs.C AS ec,	   
       CASE 
           WHEN SUM(injection.value) <= SUM(consumption.value) THEN 
                SUM(injection.value) * tariffs.CU * (-1)
           ELSE 
                SUM(consumption.value) * tariffs.CU * (-1)
       END AS ee1,
       (SELECT total_ee2 FROM total_ee) AS ee2 -- Se agrega el total de ee2 aquí
FROM records
JOIN consumption ON records.id_record = consumption.id_record
JOIN injection ON records.id_record = injection.id_record
JOIN services ON records.id_service = services.id_service
JOIN tariffs 
    ON tariffs.id_market = services.id_market 
    AND tariffs.voltage_level = services.voltage_level
    AND (
        -- Si voltage_level NO es 2 ni 3, comparar cdi
        (tariffs.voltage_level NOT IN (2,3) AND tariffs.cdi = services.cdi)
        -- Si voltage_level ES 2 o 3, ignorar cdi
        OR tariffs.voltage_level IN (2,3)
    )
WHERE records.id_service = $1 
  AND records.record_timestamp >= $2
  AND records.record_timestamp < $3
GROUP BY records.id_service, services.id_market, services.cdi, services.voltage_level,
         tariffs.cu, tariffs.c;
"""

GET_STATISTICS_QUERY = """
SELECT records.id_service, 
        SUM(consumption.value) AS total_consumption,
        SUM(injection.value) AS total_injection,
        (SUM(consumption.value) / COUNT(records.id_record)) AS avg_hourly_consumption,
        (SUM(injection.value) / COUNT(records.id_record)) AS avg_hourly_injection,
        (SUM(injection.value)-SUM(consumption.value)) AS net_balance
FROM records
JOIN consumption ON records.id_record = consumption.id_record
JOIN injection ON records.id_record = injection.id_record
WHERE records.id_service = $1
        AND records.record_timestamp >= $2
        AND records.record_timestamp < $3  
GROUP BY records.id_service      
"""

GET_LOAD_QUERY = """
SELECT records.record_timestamp AS date, 
       SUM(consumption.value) AS total_load_kwh
FROM records
JOIN consumption ON records.id_record = consumption.id_record
WHERE records.record_timestamp >= $1
      AND records.record_timestamp < $2  
GROUP BY records.record_timestamp
ORDER BY records.record_timestamp
"""

GET_EA_QUERY = """
SELECT records.id_service, 
        services.id_market, services.cdi, services.voltage_level,
        SUM(consumption.value) AS total_consumption,
        tariffs.CU,
        SUM(consumption.value) * tariffs.CU AS ea
        FROM records
JOIN consumption ON records.id_record = consumption.id_record
JOIN services ON records.id_service = services.id_service
JOIN tariffs
    ON (tariffs.id_market = services.id_market AND tariffs.voltage_level = services.voltage_level)
    OR (tariffs.id_market = services.id_market AND tariffs.voltage_level NOT IN (2,3) AND tariffs.cdi = services.cdi)
WHERE records.id_service = $1
        AND records.record_timestamp >= $2
        AND records.record_timestamp < $3  
GROUP BY records.id_service, tariffs.CU, services.id_market,services.cdi, services.voltage_level
"""

GET_EC_QUERY = """
SELECT records.id_service, 
        services.id_market, services.cdi, services.voltage_level,
        SUM(injection.value) AS total_injection,
        tariffs.C,
        SUM(injection.value) * tariffs.C AS ec
FROM records
JOIN injection ON records.id_record = injection.id_record
JOIN services ON records.id_service = services.id_service
JOIN tariffs
      ON (tariffs.id_market = services.id_market AND tariffs.voltage_level = services.voltage_level)
      OR (tariffs.id_market = services.id_market AND tariffs.voltage_level NOT IN (2,3) AND tariffs.cdi = services.cdi)
WHERE records.id_service = $1
      AND records.record_timestamp >= $2
      AND records.record_timestamp < $3  
GROUP BY records.id_service, tariffs.CU, services.id_market,services.cdi, services.voltage_level, tariffs.c
"""

GET_EE1_QUERY = """
SELECT records.id_service,        
       SUM(injection.value) AS total_injection,
       SUM(consumption.value) AS total_consumption,
       tariffs.CU,
       CASE 
       WHEN SUM(injection.value) <= SUM(consumption.value) THEN 
            SUM(injection.value) * tariffs.CU * (-1)
       ELSE 
            SUM(consumption.value) * tariffs.CU * (-1)
       END AS ee1
FROM records
JOIN consumption ON records.id_record = consumption.id_record
JOIN injection ON records.id_record = injection.id_record
JOIN services ON records.id_service = services.id_service
JOIN tariffs
     ON (tariffs.id_market = services.id_market AND tariffs.voltage_level = services.voltage_level)
     OR (tariffs.id_market = services.id_market AND tariffs.voltage_level NOT IN (2,3) AND tariffs.cdi = services.cdi)
WHERE records.id_service = $1
      AND records.record_timestamp >= $2
      AND records.record_timestamp < $3  
GROUP BY records.id_service, tariffs.CU
"""

GET_EE2_QUERY = """
WITH data AS (
    SELECT 
		records.id_service,
        records.record_timestamp, 
        injection.value AS hourly_injection,
        SUM(injection.value) OVER (ORDER BY records.record_timestamp) AS cumulative_injection,
        SUM(consumption.value) OVER () AS total_consumption,
        xm_data_hourly_per_agent.value AS invoice_factor,
        CASE 
            WHEN SUM(injection.value) OVER (ORDER BY records.record_timestamp) <= 
                 SUM(consumption.value) OVER () THEN 0
            ELSE 
                 (SUM(consumption.value) OVER ()) - SUM(injection.value) OVER ()
        END AS first_occurrence_flag
    FROM records
    JOIN injection ON records.id_record = injection.id_record
    JOIN consumption ON records.id_record = consumption.id_record
    JOIN xm_data_hourly_per_agent ON records.record_timestamp = xm_data_hourly_per_agent.record_timestamp    
    WHERE records.id_service = $1
      AND records.record_timestamp >= $2
      AND records.record_timestamp < $3 
),
ee2_data AS (
    SELECT 
		id_service,
        record_timestamp,
        hourly_injection,
        cumulative_injection,
        total_consumption,	   
        CASE 
            WHEN cumulative_injection <= total_consumption THEN 0
            WHEN cumulative_injection > total_consumption 
                 AND cumulative_injection = (SELECT MIN(cumulative_injection) FROM data WHERE cumulative_injection > total_consumption) 
            THEN cumulative_injection - total_consumption 
            ELSE hourly_injection 
        END AS ee2_without_invoice,
        invoice_factor,
        CASE 
            WHEN cumulative_injection <= total_consumption THEN 0
            WHEN cumulative_injection > total_consumption 
                 AND cumulative_injection = (SELECT MIN(cumulative_injection) FROM data WHERE cumulative_injection > total_consumption) 
            THEN (cumulative_injection - total_consumption) * invoice_factor 
            ELSE hourly_injection * invoice_factor
        END AS ee2	   
    FROM data
)
SELECT 
	id_service,
    SUM(ee2) AS ee2
FROM ee2_data
GROUP BY id_service;
"""