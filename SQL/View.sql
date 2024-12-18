-- view phân tích giá 

-- từ đây có thể vẽ biểu đồ nến, biểu đồ biến động giá, biến động khối lượng giao dịch
CREATE OR REPLACE VIEW price_analysis_view AS
SELECT
    dd.date_id,
    dd.day,
    dd.month,
    dd.year,
    dc.ma_sic,
    dc.ten_cong_ty,
    dc.san_niem_yet,
    fph.open,
    fph.hight,
    fph.low,
    fph.close,
	fph.volume
FROM
    fact_price_history fph
JOIN 
    dim_date dd ON fph.date_id = dd.date_id
JOIN
    dim_company dc ON fph.ma_sic = dc.ma_sic;


--view phan bố giá

CREATE OR REPLACE VIEW price_distribution_view AS
SELECT
    dc.ma_sic,
    dc.san_niem_yet,
    MIN(fph.close) AS min_close,
    MAX(fph.close) AS max_close,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY fph.close) AS percentile_25,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY fph.close) AS percentile_75,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fph.close) AS median_close,
    AVG(fph.volume) AS average_volume
FROM
    fact_price_history fph
JOIN
    dim_company dc ON fph.ma_sic = dc.ma_sic
GROUP BY
    dc.ma_sic;

-- View financials
CREATE VIEW financials_report_view AS
SELECT
	ff.ma_sic,
	ff.ma_tai_khoan,
	ff.gia_tri,
	dc.ten_cong_ty,
	dc.san_niem_yet,
	dt.time_period_id,
	dt.nam,
	dt.quy
FROM
    fact_financials ff
JOIN
    dim_account da ON ff.ma_tai_khoan = da.ma_tai_khoan
JOIN
    dim_company dc ON ff.ma_sic = dc.ma_sic
JOIN
    dim_time_period dt ON ff.time_period_id = dt.time_period_id



    
