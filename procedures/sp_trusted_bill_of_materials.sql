CREATE OR REPLACE PROCEDURE boa_vista_procedure.sp_trusted_bill_of_materials()
BEGIN
CREATE OR REPLACE VIEW boa_vista_view.bill_of_materials AS
SELECT
  tube_assembly_id,
   CASE
    WHEN component_id_1 = "NA" THEN NULL
  ELSE component_id_1 
  END AS component_id_1,
  CASE
    WHEN quantity_1 = "NA" THEN NULL 
  ELSE CAST(quantity_1 AS INT64) 
  END AS quantity_1,
   CASE
    WHEN component_id_2 = "NA" THEN NULL
  ELSE component_id_2 
  END AS component_id_2,
   CASE
    WHEN quantity_2 = "NA" THEN NULL
  ELSE CAST(quantity_2 AS INT64)
  END AS quantity_2, 
  CASE
    WHEN component_id_3 = "NA" THEN NULL
  ELSE component_id_3 
  END AS component_id_3,
   CASE
    WHEN quantity_3 = "NA" THEN NULL
  ELSE CAST(quantity_3 AS INT64) 
  END AS quantity_3,
   CASE
    WHEN component_id_4 = "NA" THEN NULL
  ELSE component_id_4 
  END AS component_id_4,
  CASE
    WHEN quantity_4 = "NA" THEN NULL
  ELSE CAST(quantity_4 AS INT64) 
  END AS quantity_4,
  CASE
    WHEN component_id_5 = "NA" THEN NULL
  ELSE component_id_5 
  END AS component_id_5,
  CASE
    WHEN quantity_5 = "NA" THEN NULL
  ELSE CAST(quantity_5 AS INT64) 
  END AS quantity_5,
    CASE
    WHEN component_id_6 = "NA" THEN NULL
  ELSE component_id_6 
  END AS component_id_6,
   CASE
    WHEN quantity_6 = "NA" THEN NULL
  ELSE CAST(quantity_6 AS INT64) 
  END AS quantity_6,
   CASE
    WHEN component_id_7 = "NA" THEN NULL
  ELSE component_id_7 
  END AS component_id_7,
   CASE
    WHEN quantity_7 = "NA" THEN NULL
  ELSE CAST(quantity_7 AS INT64) 
  END AS quantity_7,
  CASE
    WHEN component_id_8	 = "NA" THEN NULL
  ELSE component_id_8	 
  END AS component_id_8	,
  CASE
    WHEN quantity_8	 = "NA" THEN NULL
  ELSE CAST(quantity_8 AS INT64)	 
  END AS quantity_8	
  FROM `boa_vista.bill_of_materials`;
WHERE DATE(_PARTITIONTIME) = DATE((SELECT max(_PARTITIONTIME) as maximo from boa_vista.price_quote))
END;