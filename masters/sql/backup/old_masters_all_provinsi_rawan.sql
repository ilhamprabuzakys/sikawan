SELECT
    row_number() OVER () AS id,
    provinsi.id AS provinsi_id,
    provinsi.nama_provinsi,
    desa_count.total_desa AS total_desa,
    COALESCE(total_2023.total, 0) AS total_2023,
    COALESCE(total_2022.total, 0) AS total_2022,
    COALESCE(total_2021.total, 0) AS total_2021,
    COALESCE(bahaya_2023.total, 0) AS bahaya_2023,
    COALESCE(waspada_2023.total, 0) AS waspada_2023,
    COALESCE(siaga_2023.total, 0) AS siaga_2023,
    COALESCE(aman_2023.total, 0) AS aman_2023,
    COALESCE(bahaya_2022.total, 0) AS bahaya_2022,
    COALESCE(waspada_2022.total, 0) AS waspada_2022,
    COALESCE(siaga_2022.total, 0) AS siaga_2022,
    COALESCE(aman_2022.total, 0) AS aman_2022,
    COALESCE(bahaya_2021.total, 0) AS bahaya_2021,
    COALESCE(waspada_2021.total, 0) AS waspada_2021,
    COALESCE(siaga_2021.total, 0) AS siaga_2021,
    COALESCE(aman_2021.total, 0) AS aman_2021
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
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2023 AND kawasan.status = 'BAHAYA')::int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS bahaya_2023 ON provinsi.id = CAST(bahaya_2023.provinsi AS bigint)
LEFT JOIN
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2023 AND kawasan.status = 'WASPADA')::int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS waspada_2023 ON provinsi.id = CAST(waspada_2023.provinsi AS bigint)
LEFT JOIN
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2023 AND kawasan.status = 'SIAGA')::int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS siaga_2023 ON provinsi.id = CAST(siaga_2023.provinsi AS bigint)
LEFT JOIN
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2023 AND kawasan.status = 'AMAN')::int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS aman_2023 ON provinsi.id = CAST(aman_2023.provinsi AS bigint)
LEFT JOIN
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2022 AND kawasan.status = 'BAHAYA')::int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS bahaya_2022 ON provinsi.id = CAST(bahaya_2022.provinsi AS bigint)
LEFT JOIN
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2022 AND kawasan.status = 'WASPADA')::int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS waspada_2022 ON provinsi.id = CAST(waspada_2022.provinsi AS bigint)
LEFT JOIN
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2022 AND kawasan.status = 'SIAGA')::int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS siaga_2022 ON provinsi.id = CAST(siaga_2022.provinsi AS bigint)
LEFT JOIN
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2022 AND kawasan.status = 'AMAN')::int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS aman_2022 ON provinsi.id = CAST(aman_2022.provinsi AS bigint)
LEFT JOIN
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2021 AND kawasan.status = 'BAHAYA')::int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS bahaya_2021 ON provinsi.id = CAST(bahaya_2021.provinsi AS bigint)
LEFT JOIN
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2021 AND kawasan.status = 'WASPADA')::int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS waspada_2021 ON provinsi.id = CAST(waspada_2021.provinsi AS bigint)
LEFT JOIN
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2021 AND kawasan.status = 'SIAGA')::int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS siaga_2021 ON provinsi.id = CAST(siaga_2021.provinsi AS bigint)
LEFT JOIN
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2021 AND kawasan.status = 'AMAN')::int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS aman_2021 ON provinsi.id = CAST(aman_2021.provinsi AS bigint)
LEFT JOIN
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2023) :: int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS total_2023 ON provinsi.id = CAST(total_2023.provinsi AS bigint)
LEFT JOIN
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2022) :: int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS total_2022 ON provinsi.id = CAST(total_2022.provinsi AS bigint)
LEFT JOIN
    (
        SELECT
            desa.provinsi,
            SUM((kawasan.tahun::integer = 2021) :: int) AS total
        FROM
            masters_db_desa AS desa
        LEFT JOIN
            masters_kawasan_rawan AS kawasan ON desa.id = kawasan.desa_id
        GROUP BY
            desa.provinsi
    ) AS total_2021 ON provinsi.id = CAST(total_2021.provinsi AS bigint)
ORDER BY
    provinsi.id ASC;
