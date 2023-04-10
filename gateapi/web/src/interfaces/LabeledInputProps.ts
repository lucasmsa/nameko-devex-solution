export interface LabeledInputProps {
	label: string
	type: string
	placeholder: string
	options: LabeledInputOption[]
	icon: string
	value: string
	readonly: boolean
}

interface LabeledInputOption {
	value: string
	label: string
}
