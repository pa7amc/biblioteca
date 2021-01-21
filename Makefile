.PHONY: init docker run clean empty emp

init:
	@rm -rf scripts/db.sqlite3
	@python scripts/init_db.py
	@mv scripts/db.sqlite3 .
	
clean:
	@rm -rf db.sqlite3

emp:
	@rm -rf scripts/db.sqlite3
	@python scripts/init_db_clean.py
	@mv scripts/db.sqlite3 .
	
run: clean init
	@python app.py

empty: clean emp
	@python app.py
	
docker: clean init
	docker build -t alphabeta .
	docker run -p 5000:5000 alphabeta