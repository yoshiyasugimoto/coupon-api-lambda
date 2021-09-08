deploy:
	sls deploy --stage production

local_list:
	curl http://localhost:3000/production

local_post:
	curl -X POST http://localhost:3000/production/post

invoke_post:
	sls invoke --function post
