-- Script para criação de índice no banco de dados Amazon

-- TESTE 1

-- Sem Índice

-- Desabilita uso de index scan para forçar uso de varredura sequencial
SET enable_indexscan = off;
EXPLAIN ANALYZE
SELECT * FROM amazon.pedido WHERE ClienteID = 200;
-- Habilita de novo após o teste
SET enable_indexscan = on;

-- Índice para otimizar a consulta de pedidos por cliente
CREATE INDEX idx_pedido_cliente ON amazon.pedido (ClienteID);

-- Comando de verificação de performance depois
EXPLAIN ANALYZE SELECT * FROM amazon.pedido WHERE ClienteID = 200;



-- TESTE 2

-- Sem índice
SET enable_indexscan = off;

EXPLAIN ANALYZE
SELECT *
FROM amazon.pedido
WHERE ClienteID = 15
ORDER BY DataPedFeito;

SET enable_indexscan = on;

-- Índice para otimizar a consulta de pedidos por cliente
CREATE INDEX idx_pedido_cliente ON amazon.pedido (ClienteID);

-- Comando de verificação de performance depois
EXPLAIN ANALYZE
SELECT *
FROM amazon.pedido
WHERE ClienteID = 15
ORDER BY DataPedFeito;


