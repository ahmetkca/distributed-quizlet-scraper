build:
	docker build -t scrape_request_service:latest ./ScrapeRequestService
	docker build -t scraper_service:latest ./ScraperService

up:
	docker compose up -d --build

down:
	docker compose down

recompose: down up

recompose-build: down build up


