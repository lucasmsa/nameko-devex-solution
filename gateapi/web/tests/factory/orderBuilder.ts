import { OrderDetails } from '../../src/interfaces/OrderDetails'

export const orderBuilder = (
	overrides?: Partial<OrderDetails>
): OrderDetails => ({
	image: 'http://www.example.com/airship/images/the_odyssey.jpg',
	quantity: 3,
	price: '200',
	product_id: 'spacy',
	id: 1,
	product: {
		id: 'spacy',
		title: 'Dir Spacyel',
		maximum_speed: 1000,
		passenger_capacity: 10,
		in_stock: 10,
	},
	...overrides,
})
