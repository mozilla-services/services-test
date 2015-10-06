build_docker:
	docker build -t zap-cli .

run_docker: build_docker
	docker run -u zap -i zap-cli zap-cli quick-scan -sc -o "-config api.disablekey=true" -s xss "$(url)"
