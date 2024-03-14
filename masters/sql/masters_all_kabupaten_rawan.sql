WITH totals AS (
    SELECT desa.kabupaten::bigint AS kabupaten_id,
           (sum((((kawasan.tahun)::integer = 2023) AND ((kawasan.status)::text = 'BAHAYA'::text))::integer)) AS bahaya_2023,
           (sum((((kawasan.tahun)::integer = 2023) AND ((kawasan.status)::text = 'WASPADA'::text))::integer)) AS waspada_2023,
           (sum((((kawasan.tahun)::integer = 2023) AND ((kawasan.status)::text = 'SIAGA'::text))::integer)) AS siaga_2023,
           (sum((((kawasan.tahun)::integer = 2023) AND ((kawasan.status)::text = 'AMAN'::text))::integer)) AS aman_2023,
           (sum((((kawasan.tahun)::integer = 2022) AND ((kawasan.status)::text = 'BAHAYA'::text))::integer)) AS bahaya_2022,
           (sum((((kawasan.tahun)::integer = 2022) AND ((kawasan.status)::text = 'WASPADA'::text))::integer)) AS waspada_2022,
           (sum((((kawasan.tahun)::integer = 2022) AND ((kawasan.status)::text = 'SIAGA'::text))::integer)) AS siaga_2022,
           (sum((((kawasan.tahun)::integer = 2022) AND ((kawasan.status)::text = 'AMAN'::text))::integer)) AS aman_2022,
           (sum((((kawasan.tahun)::integer = 2021) AND ((kawasan.status)::text = 'BAHAYA'::text))::integer)) AS bahaya_2021,
           (sum((((kawasan.tahun)::integer = 2021) AND ((kawasan.status)::text = 'WASPADA'::text))::integer)) AS waspada_2021,
           (sum((((kawasan.tahun)::integer = 2021) AND ((kawasan.status)::text = 'SIAGA'::text))::integer)) AS siaga_2021,
           (sum((((kawasan.tahun)::integer = 2021) AND ((kawasan.status)::text = 'AMAN'::text))::integer)) AS aman_2021,
           (sum((((kawasan.tahun)::integer = 2023))::integer)) AS total_2023,
           (sum((((kawasan.tahun)::integer = 2022))::integer)) AS total_2022,
           (sum((((kawasan.tahun)::integer = 2021))::integer)) AS total_2021
    FROM masters_db_desa desa
    LEFT JOIN masters_kawasan_rawan kawasan ON desa.id = kawasan.desa_id
    GROUP BY desa.kabupaten::bigint
)
SELECT row_number() OVER () AS id,
    provinsi.id AS provinsi_id,
    kabupaten.id AS kabupaten_id,
    provinsi.nama_provinsi, -- Menambahkan kolom nama_provinsi dari tabel masters_data_provinsi
    kabupaten.nama_kabupaten,
    desa_count.total_desa,
    COALESCE(total_2023, 0) AS total_2023,
    COALESCE(total_2022, 0) AS total_2022,
    COALESCE(total_2021, 0) AS total_2021,
    COALESCE(bahaya_2023, 0) AS bahaya_2023,
    COALESCE(waspada_2023, 0) AS waspada_2023,
    COALESCE(siaga_2023, 0) AS siaga_2023,
    COALESCE(aman_2023, 0) AS aman_2023,
    COALESCE(bahaya_2022, 0) AS bahaya_2022,
    COALESCE(waspada_2022, 0) AS waspada_2022,
    COALESCE(siaga_2022, 0) AS siaga_2022,
    COALESCE(aman_2022, 0) AS aman_2022,
    COALESCE(bahaya_2021, 0) AS bahaya_2021,
    COALESCE(waspada_2021, 0) AS waspada_2021,
    COALESCE(siaga_2021, 0) AS siaga_2021,
    COALESCE(aman_2021, 0) AS aman_2021
FROM masters_data_kabupaten kabupaten
LEFT JOIN masters_data_provinsi provinsi ON kabupaten.provinsi_id = provinsi.id -- Melakukan join dengan tabel masters_data_provinsi
LEFT JOIN (SELECT kabupaten::bigint, COUNT(*) AS total_desa FROM masters_db_desa GROUP BY kabupaten) desa_count ON kabupaten.id = desa_count.kabupaten
LEFT JOIN totals ON kabupaten.id = totals.kabupaten_id
ORDER BY kabupaten.id;