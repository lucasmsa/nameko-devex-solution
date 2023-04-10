export interface OrderDetails {
	id: number
	image: string
	price: string
	product_id: string
	quantity: number
	product: Product
}

interface Product {
	id: string
	title: string
	maximum_speed: number
	passenger_capacity: number
	in_stock: number
}
