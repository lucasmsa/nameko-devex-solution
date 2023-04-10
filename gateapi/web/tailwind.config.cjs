module.exports = {
	content: ['./src/**/*.html', './src/**/*.svelte'],
	theme: {
		screens: {
			'md-custom': '870px',
		},
		extend: {
			colors: {
				darkViolet: '#35344C',
				lightViolet: '#3F25C8',
			},
			fontFamily: {
				amplitudeWide: ['Amplitude Wide'],
				amplitudeWideBook: ['Amplitude Wide Book'],
				inter: ['Inter'],
			},
		},
	},
	plugins: [],
}
