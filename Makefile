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

# local_post:
# 	curl -X POST -H "Content-Type: multipart/form-data" -F "image=@coupon-imges/coupon-img-1/coupon-img-1.png" \
# 	-F "image=@coupon-imges/coupon-img-1/qr-code-coupon-img-1.png" \
# 	http://localhost:3000/production/post 

# local_post:
# 	curl -X POST -H "Content-Type: application/json" \
# 	-d '{"image" : $( base64 coupon-imges/coupon-img-1/coupon-img-1.png )}' \
# 	http://localhost:3000/production/post 
# local_post:
# 	curl -X POST -H 'Content-type: image/png' --data-binary "@coupon-imges/coupon-img-1/coupon-img-1.png" http://localhost:3000/production/post
local_post:
	curl -X POST -H "Content-Type: application/json" -d @coupon-img-1.txt http://localhost:3000/production/post

invoke_post:
	sls invoke --function post

# curl -X POST -H "Content-Type: application/json" -d '{"image" : "'"$( base64 coupon-imges/coupon-img-1/qr-code-coupon-img-1.png)"'"}' http://localhost:3000/production/post
# curl -X POST -H "Content-Type: application/json" -d "'"$( base64 -e coupon-imges/coupon-img-1/qr-code-coupon-img-1.png)"'" http://localhost:3000/production/post
