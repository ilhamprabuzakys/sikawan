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
            json_build_array(data_provinsi.longitude, data_provinsi.latitude)
        ),
        'properties',
        json_build_object(
            'kd_prov',
            data_provinsi.provinsi,
            'provinsi',
            data_provinsi.nama_provinsi,
            'provinsi_singkat',
            data_provinsi.provinsi_singkat,
            'line_geom',
            data_provinsi.line_geom,
            'aman',
            kawasan.aman,
            'siaga',
            kawasan.siaga,
            'waspada',
            kawasan.waspada,
            'bahaya',
            kawasan.bahaya,
            'kotak',
            json_build_array(
                data_provinsi.longitude2,
                data_provinsi.latitude2
            )
        )
    ) AS geom,
    kawasan.tahun,
    data_provinsi.provinsi
FROM
    masters_data_provinsi data_provinsi,
    (
        SELECT
            row_number() OVER () AS id,
            data.nama_provinsi,
            data.provinsi,
            sum(data.siaga) AS siaga,
            sum(data.bahaya) AS bahaya,
            sum(data.waspada) AS waspada,
            sum(data.aman) AS aman,
            data.tahun
        FROM
            (
                SELECT
                    b.nama_provinsi,
                    b.provinsi,
                    a.tahun,
                    CASE
                        WHEN ((a.status) :: text = 'SIAGA' :: text) THEN 1
                        ELSE 0
                    END AS siaga,
                    CASE
                        WHEN ((a.status) :: text = 'BAHAYA' :: text) THEN 1
                        ELSE 0
                    END AS bahaya,
                    CASE
                        WHEN ((a.status) :: text = 'WASPADA' :: text) THEN 1
                        ELSE 0
                    END AS waspada,
                    CASE
                        WHEN ((a.status) :: text = 'AMAN' :: text) THEN 1
                        ELSE 0
                    END AS aman
                FROM
                    masters_kawasan_rawan a,
                    masters_db_desa b,
                    masters_data_provinsi c
                WHERE
                    (
                        (a.desa_id = (b.desa) :: bigint)
                        AND ((b.provinsi) :: text = (c.provinsi) :: text)
                    )
            ) data
        GROUP BY
            data.nama_provinsi,
            data.provinsi,
            data.tahun
    ) kawasan
WHERE
    (
        (data_provinsi.provinsi) :: text = (kawasan.provinsi) :: text
    );