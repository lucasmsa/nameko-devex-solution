<script>
	import { page } from '$app/stores'
</script>

<svelte:head>
	<title>Error Page</title>
</svelte:head>

<div
	class="pt-8 font-amplitudeWide text-3xl items-center justify-center flex mx-auto flex-col"
>
	<h1 id="status-code">{$page.status}</h1>
	<h1 id="error-message">{$page.error.message}</h1>
</div>
