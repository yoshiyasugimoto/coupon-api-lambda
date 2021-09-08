deploy:
	sls deploy --stage production

local_list:
	sls invoke local --function list

local_post:
	sls invoke local --function post

invoke_post:
	sls invoke --function post
