import { error as svelteError } from '@sveltejs/kit'
import { API_URL, ID } from '../../constants/apiUrl'

export async function load({ fetch }) {
	try {
		const orderDetailsUrl = `${API_URL}/orders/${ID}`
		const response = await fetch(orderDetailsUrl)

		if (!response.ok) {
			throw svelteError(response.status, 'Request to the external API failed!')
		}

		const { order_details: orderDetails } = await response.json()

		return {
			orderDetails,
		}
	} catch (error) {
		throw svelteError(
			error.status || 500,
			error.body.message || 'Internal server error'
		)
	}
}
