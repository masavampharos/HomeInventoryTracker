INSERT INTO consumption_log (id, item_id, quantity, timestamp) VALUES
(1, 3, 1, '2024-12-07 16:20:07.282501');

-- シーケンスの現在値を設定
SELECT setval('consumption_log_id_seq', 1, true);
SELECT setval('item_id_seq', 26, true); 