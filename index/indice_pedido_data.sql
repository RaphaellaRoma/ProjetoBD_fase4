-- Script para criação de índice no banco de dados Amazon

-- TESTE 1

-- Sem índice
SET enable_indexscan = off;
EXPLAIN ANALYZE
SELECT * FROM amazon.pedido
WHERE DataPedFeito BETWEEN '2023-01-01' AND '2023-12-31';
SET enable_indexscan = on;

-- índice para otimizar a buscaa de pedidos com base na data
CREATE INDEX idx_pedido_data ON amazon.pedido (DataPedFeito);

-- Comando de verificação de performance depois
EXPLAIN ANALYZE
SELECT * FROM amazon.pedido
WHERE DataPedFeito BETWEEN '2023-01-01' AND '2023-12-31';


-- TESTE 2

-- Sem Índice
SET enable_indexscan = off;
EXPLAIN ANALYZE
SELECT * FROM amazon.pedido 
WHERE DataPedFeito >= '2025-01-01';
SET enable_indexscan = on;

-- Comando de verificação de performance depois
EXPLAIN ANALYZE
SELECT * FROM amazon.pedido 
WHERE DataPedFeito >= '2025-01-01';