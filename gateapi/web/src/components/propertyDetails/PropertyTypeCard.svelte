<script lang="ts">
	import type { PropertyTypeCardProps } from '../../interfaces/PropertyTypeCardProps'
	export let data: Partial<PropertyTypeCardProps> = {}

	export let { name, icon, selected = false } = data

	let iconSource: string = icon

	$: {
		iconSource = selected ? icon.split('.svg')[0] + '-selected.svg' : icon
	}
</script>

<button
	class={`transition-colors flex cursor-pointer items-center outline-none justify-center rounded w-full h-[72px] border-solid border-[1px] ${
		selected
			? 'bg-[#F3F1FE] border-lightViolet text-lightViolet'
			: 'border-[#C3C1D7]'
	}`}
	on:click
>
	<div class="flex items-center gap-3 max-md-custom:w-[146px]">
		<img class="h-8 w-8 stroke-white" src={iconSource} alt={`${name} icon`} />
		<p class={`font-amplitudeWide text-medium`}>
			{name}
		</p>
	</div>
</button>
