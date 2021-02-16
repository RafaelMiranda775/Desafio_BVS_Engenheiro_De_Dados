CREATE OR REPLACE PROCEDURE
  boa_vista_procedure.sp_trusted_comp_boss()
BEGIN
CREATE OR REPLACE VIEW
  boa_vista_view.comp_boss AS
SELECT
  component_id,
  component_type_id,
  CASE
    WHEN type = "NA" THEN NULL
  ELSE
  CAST(type AS STRING)
END
  AS type,
  connection_type_id,
  outside_shape,
  base_type,
  CASE
    WHEN height_over_tube = "NA" THEN NULL
  ELSE
  CAST(height_over_tube AS FLOAT64)
END
  AS height_over_tube,
  CASE
    WHEN bolt_pattern_long = "NA" THEN NULL
  ELSE
  CAST(bolt_pattern_long AS FLOAT64)
END
  AS bolt_pattern_long,
  CASE
    WHEN bolt_pattern_wide = "NA" THEN NULL
  ELSE
  CAST(bolt_pattern_wide AS FLOAT64)
END
  AS bolt_pattern_wide,
  groove,
  CASE
    WHEN base_diameter = "NA" THEN NULL
  ELSE
  CAST(base_diameter AS FLOAT64)
END
  AS base_diameter,
  CASE
    WHEN shoulder_diameter = "NA" THEN NULL
  ELSE
  CAST(shoulder_diameter AS FLOAT64)
END
  AS shoulder_diameter,
  unique_feature,
  orientation,
  CASE
    WHEN weight = "NA" THEN NULL
  ELSE
  CAST(weight AS FLOAT64)
END
  AS weight
FROM
  `boa_vista.comp_boss`
WHERE DATE(_PARTITIONTIME) = DATE((SELECT max(_PARTITIONTIME) as maximo from boa_vista.price_quote));
END
  ;