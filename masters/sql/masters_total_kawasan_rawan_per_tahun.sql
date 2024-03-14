SELECT
    row_number() OVER () AS id,
    subquery.tahun,
    subquery.bahaya + subquery.waspada + subquery.siaga + subquery.aman AS total,
    subquery.bahaya,
    subquery.waspada,
    subquery.siaga,
    subquery.aman
FROM
    (
        SELECT
            '2021' :: text AS tahun,
            sum(masters_all_provinsi_rawan.bahaya_2021) AS bahaya,
            sum(masters_all_provinsi_rawan.waspada_2021) AS waspada,
            sum(masters_all_provinsi_rawan.siaga_2021) AS siaga,
            sum(masters_all_provinsi_rawan.aman_2021) AS aman
        FROM
            masters_all_provinsi_rawan
        UNION
        SELECT
            '2022' :: text AS tahun,
            sum(masters_all_provinsi_rawan.bahaya_2022) AS bahaya,
            sum(masters_all_provinsi_rawan.waspada_2022) AS waspada,
            sum(masters_all_provinsi_rawan.siaga_2022) AS siaga,
            sum(masters_all_provinsi_rawan.aman_2022) AS aman
        FROM
            masters_all_provinsi_rawan
        UNION
        SELECT
            '2023' :: text AS tahun,
            sum(masters_all_provinsi_rawan.bahaya_2023) AS bahaya,
            sum(masters_all_provinsi_rawan.waspada_2023) AS waspada,
            sum(masters_all_provinsi_rawan.siaga_2023) AS siaga,
            sum(masters_all_provinsi_rawan.aman_2023) AS aman
        FROM
            masters_all_provinsi_rawan
    ) subquery;

--- OLD:
SELECT
    row_number() OVER () AS id,
    subquery.tahun,
    subquery.total,
    subquery.bahaya,
    subquery.waspada,
    subquery.siaga,
    subquery.aman
FROM
    (
        SELECT
            '2021' :: text AS tahun,
            sum(masters_all_provinsi_rawan.total_2021) AS total,
            sum(masters_all_provinsi_rawan.bahaya_2021) AS bahaya,
            sum(masters_all_provinsi_rawan.waspada_2021) AS waspada,
            sum(masters_all_provinsi_rawan.siaga_2021) AS siaga,
            sum(masters_all_provinsi_rawan.aman_2021) AS aman
        FROM
            masters_all_provinsi_rawan
        UNION
        SELECT
            '2022' :: text AS tahun,
            sum(masters_all_provinsi_rawan.total_2022) AS total,
            sum(masters_all_provinsi_rawan.bahaya_2022) AS bahaya,
            sum(masters_all_provinsi_rawan.waspada_2022) AS waspada,
            sum(masters_all_provinsi_rawan.siaga_2022) AS siaga,
            sum(masters_all_provinsi_rawan.aman_2022) AS aman
        FROM
            masters_all_provinsi_rawan
        UNION
        SELECT
            '2023' :: text AS tahun,
            sum(masters_all_provinsi_rawan.total_2023) AS total,
            sum(masters_all_provinsi_rawan.bahaya_2023) AS bahaya,
            sum(masters_all_provinsi_rawan.waspada_2023) AS waspada,
            sum(masters_all_provinsi_rawan.siaga_2023) AS siaga,
            sum(masters_all_provinsi_rawan.aman_2023) AS aman
        FROM
            masters_all_provinsi_rawan
    ) subquery;