# 💻 Nameko Devex Web Test w/ SvelteKit

### ⚙️ How to run the application
```
# Install dependencies
$ npm install

# Run the application
$ npm run dev

# Run the tests 🧪
$ npm run test
```

* Notice that for the application to be ran correctly, the microservices must be running. If you have any problems running the microservices application, please refer to: [running microservices application using Docker](https://github.com/gitricko/nameko-devex/blob/master/README.md) or
[using Conda](https://github.com/gitricko/nameko-devex/blob/master/README-DevEnv.md)


### 📄 Tasks

- [x]  Style and structure the `Property details` page according to this [Figma mock](https://www.figma.com/file/DSl3CRb0uW5hyIUNE0rWPK/nameko-devex?node-id=0-1&t=U13RUERzIzCqApR9-0) using Tailwindcss
- [x]  Make a GET request to the orders API, retrieving the Order with `id` 1, displaying those details on the page

### 💢 Troubleshooting

> - Initially Had errors running the `npm run dev` command
>   - I've installed `vite` as a dev dependency with `npm i --save-dev vite`, to run the project using it
>   - Created a new `vite.config.js` file, adding a vite configuration inside of the svelte-kit project using the `sveltekit` plugin. Also, inside the `svelte.config.js` file, I've changed the `preprocessor` of `svelte-preprocess` to `vitePreprocess` from `@sveltejs/kit/vite` and removed the `methodOverride property`
>   - Furthermore, I've changed the `svelte-kit` commands to `vite` inside the `package.json` file
>   - Replaced `svelte.` on the `app.html` file to `sveltekit.`
>   - Changed the file names from `index.svelte` to `+page.svelte` as well as `_layout.svelte` to `+layout.svelte`
>   - Now the application works correctly when running the `npm run dev` command
>  - CORS Issues
>       - I was having a CORS problem when requesting the Orders service: `Error: CORS error: No 'Access-Control-Allow-Origin' header is present on the requested resource`
>       - To fix it I've added a `proxy` configuration setting for the request inside the `vite.config.js`

### ⚙️ Features

- Created `LabeledInput`, `PropertyTypeCard`, `OrderPropertyWrapper` Components. So that they can be reutilized on the application
- Used the `static/` folder to store images, due to the fact that they will be copied to the output directory during the build process, and are served by the server
- The same was done for fonts. Also, some configurations were made to the `tailwind.config.cjs` file in order to identify font-families for class recognition
- Made sure that the application works smoothly  on mobile and tablets
- Requests were made using SvelteKit's SSR capabilities, in order to fetch data from the server, pre-loading data with direct requests to the server, reducing the workload for the client
- Added Integration tests to both developed pages.
    - *These tests are integration tests because they test the interaction between multiple components of the application (such as the `PropertyDetails` component and the `PropertyTypeCard` component) to ensure they work together correctly. They also test how the user interacts with the interface and how the application responds to user input.*


### 📷 Screenshots
![Property Details page](https://i.imgur.com/eYZ3455.png)

---

![Order Details page](https://i.imgur.com/IJ76cOo.png)