-- Script para criação de índice no banco de dados Amazon

-- TESTE 1

-- Sem índice
SET enable_indexscan = off;
EXPLAIN ANALYZE
SELECT * FROM amazon.cliente WHERE NomeCliente ILIKE 'A%';
SET enable_indexscan = on;

-- Índice para otimizar a consulta de pedidos por cliente
CREATE INDEX idx_pedido_cliente ON amazon.pedido (ClienteID);

-- Comando de verificação de performance depois
EXPLAIN ANALYZE
SELECT * FROM amazon.cliente WHERE NomeCliente ILIKE 'A%';


-- TESTE 2

-- Sem Índice
SET enable_indexscan = off;
EXPLAIN ANALYZE
SELECT * FROM amazon.pedido WHERE ClienteID = 200;
SET enable_indexscan = on;

-- Comando de verificação de performance depois
EXPLAIN ANALYZE SELECT * FROM amazon.pedido WHERE ClienteID = 200;
