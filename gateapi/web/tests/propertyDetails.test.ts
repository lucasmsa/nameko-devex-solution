import PropertyDetails from '../src/routes/property-details/+page.svelte'
import { describe, test, expect } from 'vitest'
import { render, screen } from '@testing-library/svelte'
import userEvent from '@testing-library/user-event'

describe('Property Details page', () => {
	test('should load successfully', async () => {
		render(PropertyDetails)

		const pageTitle = screen.findByText('Property Details')

		expect(pageTitle).toBeTruthy()
	})

	test('should allow the user to select a property type', async () => {
		render(PropertyDetails)

		const propertyTypeCardButton = screen.getByRole('button', {
			name: 'Single-Family icon Single-Family',
		})

		const user = userEvent.setup()

		const enabledBorder = 'border-lightViolet'

		expect(
			!propertyTypeCardButton.classList.contains(enabledBorder)
		).toBeTruthy()

		await user.click(propertyTypeCardButton)

		expect(
			propertyTypeCardButton.classList.contains(enabledBorder)
		).toBeTruthy()
	})

	test('should allow the user to enter a unit name', async () => {
		render(PropertyDetails)

		const unitNameInput = screen.getByPlaceholderText(
			'Name and/or number'
		) as any

		const user = userEvent.setup()

		await user.type(unitNameInput, 'Unit 1')

		const inputValue = unitNameInput.value

		expect(inputValue).toBe('Unit 1')
	})

	test('should allow the user to go back to the previous page', async () => {
		window.history.pushState({}, 'Previous Page Title', '/')

		render(PropertyDetails)

		const backButton = screen.getByText('continue')

		const user = userEvent.setup()

		user.click(backButton)

		expect(window.location.pathname).toBe('/')
	})
})
