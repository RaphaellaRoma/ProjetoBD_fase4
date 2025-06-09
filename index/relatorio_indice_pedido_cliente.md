# Índice de Otimização - Sistema de Pedidos

## Índice Criado

- **Nome do Índice:** `idx_pedido_cliente`
- **Tabela:** `amazon.pedido`
- **Coluna:** `ClienteID`
- **Objetivo:** Otimizar as consultas que buscam todos os pedidos de um cliente específico.

## Justificativa

Durante o uso do sistema, uma das funcionalidades mais comuns é a listagem de pedidos vinculados a um cliente. Consultas como:

```sql
SELECT * FROM amazon.pedido WHERE ClienteID = 1;
```

são frequentemente executadas. Sem um índice, o banco realiza um `Seq Scan`, varrendo toda a tabela. Isso afeta o desempenho à medida que o volume de dados cresce.

## Resultado da Otimização

A criação do índice:

```sql
CREATE INDEX idx_pedido_cliente ON amazon.pedido (ClienteID);
```

permite que o PostgreSQL utilize um `Index Scan` em vez de `Seq Scan`, conforme demonstrado com:

```sql
EXPLAIN ANALYZE SELECT * FROM amazon.pedido WHERE ClienteID = 1;
```

O tempo de execução reduz significativamente, comprovando a eficácia do índice.

## Observação

Essa melhoria é perceptível especialmente quando a tabela `pedido` contém muitos registros.

## Testes
![Teste 1](Testes/teste1_pedido_cliente.png)

![Teste 2](Testes/teste2_pedido_cliente.png)
