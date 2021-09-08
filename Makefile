deploy:
	sls deploy --stage production

local_list:
	sls invoke local --function list

local_post:
    sls invoke local --function post --data '{"Records": ["s3": {"object":{"key": "test"}}]}'

invoke_post :
    sls invoke --function post --data '{"Records": ["s3": {"object":{"key": "test"}}]}'
