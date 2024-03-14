SELECT
    provinsi.id AS provinsi_id,
    provinsi.nama_provinsi,
    desa_count.total_desa AS total_desa,
    SUM(CASE WHEN kawasan.tahun::integer = 2023 AND kawasan.status = 'BAHAYA' THEN 1 ELSE 0 END) AS bahaya_2023,
    SUM(CASE WHEN kawasan.tahun::integer = 2023 AND kawasan.status = 'WASPADA' THEN 1 ELSE 0 END) AS waspada_2023,
    SUM(CASE WHEN kawasan.tahun::integer = 2023 AND kawasan.status = 'SIAGA' THEN 1 ELSE 0 END) AS siaga_2023,
    SUM(CASE WHEN kawasan.tahun::integer = 2023 AND kawasan.status = 'AMAN' THEN 1 ELSE 0 END) AS aman_2023,
    SUM(CASE WHEN kawasan.tahun::integer = 2022 AND kawasan.status = 'BAHAYA' THEN 1 ELSE 0 END) AS bahaya_2022,
    SUM(CASE WHEN kawasan.tahun::integer = 2022 AND kawasan.status = 'WASPADA' THEN 1 ELSE 0 END) AS waspada_2022,
    SUM(CASE WHEN kawasan.tahun::integer = 2022 AND kawasan.status = 'SIAGA' THEN 1 ELSE 0 END) AS siaga_2022,
    SUM(CASE WHEN kawasan.tahun::integer = 2022 AND kawasan.status = 'AMAN' THEN 1 ELSE 0 END) AS aman_2022,
    SUM(CASE WHEN kawasan.tahun::integer = 2021 AND kawasan.status = 'BAHAYA' THEN 1 ELSE 0 END) AS bahaya_2021,
    SUM(CASE WHEN kawasan.tahun::integer = 2021 AND kawasan.status = 'WASPADA' THEN 1 ELSE 0 END) AS waspada_2021,
    SUM(CASE WHEN kawasan.tahun::integer = 2021 AND kawasan.status = 'SIAGA' THEN 1 ELSE 0 END) AS siaga_2021,
    SUM(CASE WHEN kawasan.tahun::integer = 2021 AND kawasan.status = 'AMAN' THEN 1 ELSE 0 END) AS aman_2021,
    SUM(CASE WHEN kawasan.tahun::integer = 2023 THEN
                (CASE WHEN kawasan.status = 'BAHAYA' THEN 1 ELSE 0 END) +
                (CASE WHEN kawasan.status = 'WASPADA' THEN 1 ELSE 0 END) +
                (CASE WHEN kawasan.status = 'SIAGA' THEN 1 ELSE 0 END) +
                (CASE WHEN kawasan.status = 'AMAN' THEN 1 ELSE 0 END)
            ELSE 0 END) AS total_2023
FROM
    masters_data_provinsi AS provinsi
LEFT JOIN
    (
        SELECT
            provinsi,
            COUNT(*) AS total_desa
        FROM
            masters_db_desa
        GROUP BY
            provinsi
    ) AS desa_count ON provinsi.id = CAST(desa_count.provinsi AS bigint)
LEFT JOIN
    masters_db_desa AS desa ON provinsi.id = CAST(desa.provinsi AS bigint)
LEFT JOIN
    masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
GROUP BY
    provinsi.id,
    provinsi.nama_provinsi,
    desa_count.total_desa;