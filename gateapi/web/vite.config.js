import { sveltekit } from '@sveltejs/kit/vite'

/** @type {import('vite').UserConfig} */
const config = {
	plugins: [sveltekit()],
	test: {
		globals: true,
		environment: 'jsdom',
		include: ['src/**/*.{test.spec}.ts'],
		setupFiles: ['./setupTest.js'],
	},
	server: {
		port: 3000,
		proxy: {
			'/api': {
				target: 'http://localhost:8000',
				rewrite: (path) => path.replace(/^\/api/, ''),
				changeOrigin: true,
				secure: false,
				ws: true,
			},
		},
	},
}

export default config
