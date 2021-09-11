deploy:
	sls deploy --stage production

dev_list:
	sls invoke local --function list

offline_api:
	sls offline start

local_list:
	curl http://localhost:3000/production | jq .

# id=0000028, title=クーポン0000028(encode=%E3%82%AF%E3%83%BC%E3%83%9D%E3%83%B30000028)
local_get:
	curl  http://localhost:3000/production/0000028/%E3%82%AF%E3%83%BC%E3%83%9D%E3%83%B30000028
