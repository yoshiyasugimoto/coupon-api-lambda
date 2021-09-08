deploy:
	sls deploy --stage production

dev_list:
	sls invoke local --function list

dev_post:
	sls invoke local --function post

offline_api:
	sls offline start

local_list:
	curl http://localhost:3000/production

local_post:
	curl -X POST http://localhost:3000/production/post

invoke_post:
	sls invoke --function post
