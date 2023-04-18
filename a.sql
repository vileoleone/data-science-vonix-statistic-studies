
SELECT call_table_name.talk_secs, DATE_FORMAT( call_table_name.start_time, '%m-%d-%Y') as "Date", DATE_FORMAT( call_table_name.start_time, '%H:%i:%s') as "Time"  FROM call_table_name  WHERE call_table_name.talk_secs > 0;

SELECT 
    talk_secs, 
    UNIX_TIMESTAMP(start_time) as time_at
FROM
call_table_name
WHERE
talk_secs > 0
AND UNIX_TIMESTAMP(start_time) BETWEEN 1679691063 AND  1680099684;