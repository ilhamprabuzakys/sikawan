WITH kawasan_counts AS (
    SELECT
        masters_db_desa.nama_provinsi,
        masters_db_desa.provinsi,
        masters_kawasan_rawan.tahun,
        COUNT(*) FILTER (
            WHERE
                masters_kawasan_rawan.status = 'SIAGA'
        ) AS siaga,
        COUNT(*) FILTER (
            WHERE
                masters_kawasan_rawan.status = 'BAHAYA'
        ) AS bahaya,
        COUNT(*) FILTER (
            WHERE
                masters_kawasan_rawan.status = 'WASPADA'
        ) AS waspada,
        COUNT(*) FILTER (
            WHERE
                masters_kawasan_rawan.status = 'AMAN'
        ) AS aman
    FROM
        masters_kawasan_rawan
        JOIN masters_db_desa ON masters_kawasan_rawan.desa_id = masters_db_desa.desa :: bigint
    GROUP BY
        masters_db_desa.nama_provinsi,
        masters_db_desa.provinsi,
        masters_kawasan_rawan.tahun
),
provinsi_counts AS (
    SELECT
        provinsi :: bigint AS provinsi_id,
        COUNT(*) AS total_desa
    FROM
        masters_db_desa
    GROUP BY
        provinsi :: bigint
)
SELECT
    row_number() OVER () AS id,
    json_build_object(
        'type',
        'Feature',
        'geometry',
        json_build_object(
            'type',
            'Point',
            'coordinates',
            json_build_array(
                masters_data_provinsi.longitude,
                masters_data_provinsi.latitude
            )
        ),
        'properties',
        json_build_object(
            'kd_prov',
            masters_data_provinsi.provinsi,
            'provinsi',
            masters_data_provinsi.nama_provinsi,
            'provinsi_singkat',
            masters_data_provinsi.provinsi_singkat,
            'line_geom',
            masters_data_provinsi.line_geom,
            'aman',
            kawasan_counts.aman,
            'siaga',
            kawasan_counts.siaga,
            'waspada',
            kawasan_counts.waspada,
            'bahaya',
            kawasan_counts.bahaya,
            'kotak',
            json_build_array(
                masters_data_provinsi.longitude2,
                masters_data_provinsi.latitude2
            ),
            'total_desa',
            provinsi_counts.total_desa
        )
    ) AS geom,
    kawasan_counts.tahun,
    masters_data_provinsi.provinsi
FROM
    masters_data_provinsi
    JOIN kawasan_counts ON masters_data_provinsi.provinsi = kawasan_counts.provinsi
    JOIN provinsi_counts ON masters_data_provinsi.provinsi :: bigint = provinsi_counts.provinsi_id;