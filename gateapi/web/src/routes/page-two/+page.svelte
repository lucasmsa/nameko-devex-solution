<script lang="ts">
	import type { OrderDetails } from '../../interfaces/OrderDetails'
	import OrderPropertyWrapper from '../../components/orderDetails/OrderPropertyWrapper.svelte'

	export let data: { orderDetails: OrderDetails[] }
	export let { orderDetails: orders } = data

	function handleBackgroundUrl(imgUrl: string) {
		try {
			return `url(${imgUrl})`
		} catch (error) {
			return ``
		}
	}
</script>

<svelte:head>
	<title>Order Details</title>
</svelte:head>

<div
	class="font-amplitudeWideBook transition-all flex flex-col container mx-auto px-12 my-8 content-center justify-center gap-10"
>
	<a
		href="/"
		class="cursor-pointer font-amplitudeWide text-4xl text-center text-darkViolet border-solid border-2 border-darkViolet w-fit h-fit px-3 rounded-full"
		>{'<'}</a
	>
	<h1 class="text-5xl font-bold self-center">Order Details</h1>
	<div class="flex flex-col gap-12">
		{#each orders as order}
			<div class="bg-white rounded-lg shadow-lg">
				<div
					class="h-48 w-full bg-darkViolet rounded-t-lg"
					style={`background-image: ${handleBackgroundUrl(order.image)}`}
				/>
				<div class="p-4">
					<h2 class="text-3xl font-bold">{order.product.title}</h2>
					<div class="text-gray-700 text-xs mb-4">
						id: {order.product_id}
					</div>
					<div class="font-bold text-xl mb-4">
						Price: ${order.price}
					</div>
					<OrderPropertyWrapper>
						🗃️ Quantity: {order.quantity}
					</OrderPropertyWrapper>
					<OrderPropertyWrapper>
						🏎️ Maximum Speed: {order.product.maximum_speed}
					</OrderPropertyWrapper>
					<OrderPropertyWrapper>
						👨‍👩‍👧 Passenger Capacity: {order.product.passenger_capacity}
					</OrderPropertyWrapper>
					<OrderPropertyWrapper>
						📦 In Stock: {order.product.in_stock}
					</OrderPropertyWrapper>
				</div>
			</div>
		{/each}
	</div>
</div>
