# Kanban Frontend

## Getting Started

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM relies on the package.json file located in the `/frontend` directory of this repository. After cloning, open your terminal and run:

```
npm install
```

### Creating enviroment variables

1. Create the file `.env` on the `/frontend` directory
2. Open the `.env` file and configure the enviroment variables

```
REACT_APP_AUTH0_DOMAIN = <Auth0 application Domain>
REACT_APP_AUTH0_CLIENT_ID = <Auth0 application Client ID>
REACT_APP_AUTH0_CLIENT_SECRET = <Auth0 application Client Secret>
REACT_APP_AUTH0_AUDIENCE = <Auth0 API Identifier>
REACT_APP_API_URL = http://localhost:5000
```

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`.

```
npm start
```

Open [http://localhost:3000](http://localhost:3000) to view it in the browser.
