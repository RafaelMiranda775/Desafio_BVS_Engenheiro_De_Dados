CREATE OR REPLACE PROCEDURE
  boa_vista_procedure.sp_trusted_price_quote()
BEGIN
CREATE OR REPLACE VIEW
  boa_vista_view.price_quote AS
SELECT
  tube_assembly_id,
  supplier,
  CAST(quote_date AS DATE) AS quote_date,
  CAST(annual_usage AS INT64) AS annual_usage,
  CAST(min_order_quantity AS INT64) AS min_order_quantity,
  bracket_pricing,
  CAST(quantity AS INT64) AS quantity,
  CAST(cost AS NUMERIC) AS cost
FROM
  `boa_vista.price_quote`
WHERE DATE(_PARTITIONTIME) = DATE((SELECT max(_PARTITIONTIME) as maximo from boa_vista.price_quote));
END;