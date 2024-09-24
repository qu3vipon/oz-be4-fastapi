from fastapi import (APIRouter, Query, Path, status, HTTPException,
					 UploadFile, Form, File)

from products.response import ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])

products = [
	{"id": 1, "name": "i-Phone", "price": 1000, "image_name": None},
	{"id": 2, "name": "i-Mac", "price": 2000, "image_name": None},
	{"id": 3, "name": "Galaxy fold", "price": 1000, "image_name": None},
]

@router.get(
	"/",
	status_code=status.HTTP_200_OK,
	response_model=list[ProductResponse],
	description="전체 상품 조회 API",
)
def get_products_handler(max_price: int | None = Query(default=None, ge=100)):
	ret = []
	if max_price is not None:
		for product in products:
			if product["price"] <= max_price:
				ret.append(product)
		return [ProductResponse.build(product=product) for product in ret]
	else:
		return [ProductResponse.build(product=product) for product in products]

@router.get(
	"/{product_name}",
	status_code=status.HTTP_200_OK,
	response_model=ProductResponse,
)
def get_product_handler(product_name: str = Path(default=..., max_length=20)):
	for product in products:
		if product["name"] == product_name:
			return ProductResponse.build(product=product)

	raise HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail="Product not found",
	)


@router.patch(
	"/{product_id}",
	status_code=status.HTTP_200_OK,
	response_model=ProductResponse,
)
def patch_product_handler(
	product_id: int,
	# body: UpdateProductRequest,  # Content-type: application/json
	name: str | None = Form(default=None),
	price: int | None = Form(default=None),
	file: UploadFile | None = File(default=None),  # Content-type: multipart/form-data
):
	for product in products:
		if product["id"] == product_id:
			if name is not None:
				product["name"] = name
			if price is not None:
				product["price"] = price
			if file is not None:
				product["image_name"] = file.filename
			return ProductResponse.build(product=product)

	raise HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail="Product not found",
	)
