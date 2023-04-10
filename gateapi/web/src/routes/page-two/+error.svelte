<script>
	import { page } from '$app/stores'
	import { emojis } from '../emojis'
</script>

<svelte:head>
	<title>Error Order Details Page</title>
</svelte:head>

<div
	class="pt-8 font-amplitudeWide gap-4 items-center justify-center flex mx-auto flex-col"
>
	<h1 id="status-code" class="text-4xl">Code: {$page.status}</h1>
	<p id="error-message" class="text-3xl">Message: {$page.error.message}</p>
	<h3 id="error-emoji" class="text-5xl">
		{emojis[$page.status] ?? emojis[500]}
	</h3>
</div>
