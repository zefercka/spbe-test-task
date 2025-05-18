DROP TABLE IF EXISTS crypto_quotes;

DROP TABLE IF EXISTS crypto_tickers;

DROP TABLE IF EXISTS invest_quotes;

DROP TABLE IF EXISTS invest_tickers;

CREATE TABLE crypto_tickers (
	ticker_id SERIAL PRIMARY KEY,
	ticker_name VARCHAR(64) UNIQUE NOT NULL
);

CREATE TABLE crypto_quotes (
	quote_id SERIAL PRIMARY KEY,
	ticker_id INT NOT NULL,
	timestamp TIMESTAMP NOT NULL,
	open_price DOUBLE PRECISION NOT NULL,
	highest_price DOUBLE PRECISION NOT NULL,
	lowest_price DOUBLE PRECISION NOT NULL,
	close_price DOUBLE PRECISION,
	macd DOUBLE PRECISION,
	signal DOUBLE PRECISION,
	AO DOUBLE PRECISION,
	AC DOUBLE PRECISION,
	histogram DOUBLE PRECISION,
	FOREIGN KEY (ticker_id) REFERENCES crypto_tickers(ticker_id)
);

CREATE TABLE invest_tickers (
	ticker_id SERIAL PRIMARY KEY,
	ticker_name VARCHAR(64) UNIQUE NOT NULL
);

CREATE TABLE invest_quotes (
	quote_id SERIAL PRIMARY KEY,
	ticker_id INT NOT NULL,
	timestamp TIMESTAMP NOT NULL,
	open_price DOUBLE PRECISION NOT NULL,
	highest_price DOUBLE PRECISION NOT NULL,
	lowest_price DOUBLE PRECISION NOT NULL,
	close_price DOUBLE PRECISION,
	volume INT NOT NULL,
	diff_close_prices DOUBLE PRECISION,
	day_range DOUBLE PRECISION GENERATED ALWAYS AS (highest_price - lowest_price) STORED,
	FOREIGN KEY (ticker_id) REFERENCES invest_tickers(ticker_id)
);