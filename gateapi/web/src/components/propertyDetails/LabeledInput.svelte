<script lang="ts">
	import type { LabeledInputProps } from '../../interfaces/LabeledInputProps'

	export let {
		label,
		icon,
		options = [],
		placeholder = '',
		value = '',
		type = 'text',
		readonly = false,
	}: Partial<LabeledInputProps> = {}

	const hasOptions = options.length > 0
	const isNumberType = type === 'number'

	function handleChange(event: Event) {
		const target = event.target as HTMLInputElement
		value = target.value
	}
</script>

<section class="w-full">
	{#if label}
		<label for="input-handler" class="text-label">{label}</label>
	{/if}

	<div
		class="flex border-[#C3C1D7] border-solid border-[1px] h-12 rounded items-center p-3"
	>
		{#if icon}
			<div class="flex-shrink-0 flex items-center mr-3">
				<img class="h-full w-auto" src={icon} alt={`${label} icon`} />
			</div>
		{/if}

		{#if hasOptions}
			<select
				style="appearance: none; background-image: url('/icons/chevron-down-icon.svg'); background-position: right center; background-repeat: no-repeat; padding-right: 2rem;"
				class="cursor-pointer w-full !outline-none text-base font-amplitudeWideBook"
				{value}
				on:change={handleChange}
			>
				<option value="" disabled selected>Select</option>
				{#each options as option}
					<option class="text-darkViolet" value={option.value}
						>{option.label}</option
					>
				{/each}
			</select>
		{:else}
			<input
				type={type || 'text'}
				id="input-handler"
				{value}
				{placeholder}
				{readonly}
				on:input={handleChange}
				class={`w-full !outline-none text-base font-amplitudeWideBook 
				${isNumberType && 'placeholder:translate-x-[70%]'}`}
			/>
		{/if}
	</div>
</section>
