-- Insert initial items
INSERT INTO item (name, current_stock, minimum_stock, image_url, order_index) VALUES
('トイレットペーパー', 12, 4, 'https://images.unsplash.com/photo-1584556812952-905ffd0c611a', 1),
('ティッシュペーパー', 8, 3, 'https://images.unsplash.com/photo-1597697384801-e88c7564d7c3', 2),
('キッチンペーパー', 4, 2, 'https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec', 3),
('歯磨き粉', 2, 1, 'https://images.unsplash.com/photo-1571115764595-644a1f56a55c', 4),
('シャンプー', 2, 1, 'https://images.unsplash.com/photo-1556227702-d1e4e7b5c232', 5),
('ボディーソープ', 2, 1, 'https://images.unsplash.com/photo-1614806687394-7e093b514ce9', 6),
('食器用洗剤', 2, 1, 'https://images.unsplash.com/photo-1622503174733-c09f2b5a0c78', 7),
('ハンドソープ', 3, 1, 'https://images.unsplash.com/photo-1584351583369-6baf055b51f7', 8);

-- Insert sample consumption logs
INSERT INTO consumption_log (item_id, quantity, note, timestamp) VALUES
(1, 1, '通常使用', CURRENT_TIMESTAMP - INTERVAL '7 days'),
(2, 1, '通常使用', CURRENT_TIMESTAMP - INTERVAL '5 days'),
(3, 1, 'キッチン掃除で使用', CURRENT_TIMESTAMP - INTERVAL '3 days'),
(4, 1, '使い切り', CURRENT_TIMESTAMP - INTERVAL '2 days'); 