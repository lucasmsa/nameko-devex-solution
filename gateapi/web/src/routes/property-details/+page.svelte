<script lang="ts">
	import { writable } from 'svelte/store'
	import LabeledInput from '../../components/propertyDetails/LabeledInput.svelte'
	import PropertyTypeCard from '../../components/propertyDetails/PropertyTypeCard.svelte'
	import {
		propertyOptions,
		propertyTypeCards,
	} from '../../constants/propertyInformations'

	const selected = writable(null)
</script>

<svelte:head>
	<title>Property Details</title>
	<meta name="description" content="Property Details" />
</svelte:head>

<section
	class="flex flex-col w-full ml-auto mr-auto max-w-[908px] py-[70px] px-8"
>
	<section class="flex flex-wrap">
		<div class="flex max-md-custom:flex-col-reverse max-md-custom:gap-10">
			<div class="text-lg flex flex-col gap-3 md-custom:max-w-[410px]">
				<h2 class="font-amplitudeWide text-4xl">Property details</h2>
				<p class="font-amplitudeWideBook text-[18px] tracking-tight">
					Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
					eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
					minim veniam.
				</p>
				<div class="flex flex-col gap-4 mt-4">
					<LabeledInput label="Property Name" />
					<LabeledInput
						readonly
						label="Address"
						value={'21 Jump Street, Los Angeles, California'}
					/>
				</div>
			</div>
			<div class="md-custom:ml-20 max-md-custom:mx-auto">
				<img
					class="min-w-[340px] min-h-[220px]"
					src="/icons/property-icon.svg"
					alt="Property Icon"
				/>
			</div>
		</div>
	</section>
	<section class="flex flex-col flex-wrap my-8 gap-2">
		<p class="text-label">Property Type</p>
		<div class="flex gap-5 max-md-custom:flex-col">
			{#each propertyTypeCards as { name, icon }, index}
				<PropertyTypeCard
					{name}
					{icon}
					selected={$selected === index}
					on:click={() => {
						selected.set(index)
					}}
				/>
			{/each}
		</div>
	</section>
	<section>
		<p class="text-label">Unit info</p>
		<div
			class="flex flex-col gap-[26px] border-[#E5E5E4] border-solid border-[1px] mt-2 rounded shadow-[0_6px_16px_2px_rgb(0,0,0,0.1)] p-6"
		>
			<div class="flex gap-6 content-between max-md-custom:flex-col">
				<LabeledInput placeholder="Name and/or number" label="Unit Name" />
				<LabeledInput
					icon="/icons/dollar-icon.svg"
					label="Rent"
					type="number"
					placeholder="/mo"
				/>
				<LabeledInput
					icon="/icons/dollar-icon.svg"
					label="Deposit"
					type="number"
					placeholder="/mo"
				/>
				<LabeledInput readonly label="Lease Length (months)" value={'12'} />
			</div>
			<div class="flex gap-6 content-between max-md-custom:flex-col">
				<LabeledInput
					icon="/icons/bed-icon.svg"
					placeholder="Select"
					options={propertyOptions}
					label="Beds"
				/>
				<LabeledInput
					icon="/icons/bath-icon.svg"
					placeholder="Select"
					options={propertyOptions}
					label="Baths"
				/>
				<LabeledInput readonly label="Sq. Ft." value={'12'} />
				<LabeledInput
					icon="/icons/calendar-available-icon.svg"
					label="Available on"
					value={'11/4/2021'}
				/>
				<LabeledInput
					icon="/icons/people-icon.svg"
					placeholder="Select"
					options={propertyOptions}
					label="Vacancy"
				/>
			</div>
		</div>
	</section>
	<section class="mt-16 flex justify-between">
		<a href="/" class="btn-outline">back</a>
		<a href="/" class="btn-primary">continue</a>
	</section>
</section>
