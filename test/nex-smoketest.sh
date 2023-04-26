#!/bin/bash

# DIR="${BASH_SOURCE%/*}"
# if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
# . "$DIR/nex-include.sh"

# to ensure if 1 command fails.. build fail
set -e

# ensure prefix is pass in
if [ $# -lt 1 ] ; then
	echo "NEX smoketest needs prefix"
	echo "nex-smoketest.sh acceptance"
	exit
fi

PREFIX=$1

# check if doing local smoke test
if [ "${PREFIX}" != "local" ]; then
    echo "Remote Smoke Test in CF"
    STD_APP_URL=${PREFIX}
else
    echo "Local Smoke Test"
    STD_APP_URL=http://localhost:8000
fi

echo STD_APP_URL=${STD_APP_URL}

# Test: Create Products
echo "=== Creating a product id: bkt ==="
curl -s -XPOST  "${STD_APP_URL}/products" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"id": "bkt", "title": "The Odyssey", "passenger_capacity": 101, "maximum_speed": 5, "in_stock": 10}'
echo

# Test: Get Product
echo "=== Getting product id: bkt ==="
curl -s "${STD_APP_URL}/products/bkt" | jq .

# Test: Create Order
echo "=== Creating Order ==="
ORDER_ID=$(
    curl -s -XPOST "${STD_APP_URL}/orders" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"order_details": [{"product_id": "bkt", "price": "100000.99", "quantity": 1}]}' 
)
echo ${ORDER_ID} | jq .

ID=$(echo ${ORDER_ID} | jq '.id')

# Test: Listing Orders
echo "=== Listing Orders ==="
curl -s "${STD_APP_URL}/orders?page=1&per_page=3" | jq .

# Test: Get Order back
echo "=== Getting Order ==="
curl -s "${STD_APP_URL}/orders/${ID}" | jq .

# Test: Delete Product
echo "=== Deleting product id: bkt ==="
curl -s -XDELETE "${STD_APP_URL}/products/bkt"
echo "Product deleted"

# Test: Get Product
echo "=== Getting product id: bkt ==="
curl -s "${STD_APP_URL}/products/bkt" | jq .
