import { HelmetProvider, Helmet } from "react-helmet-async";

import Router from "./Components/Router/Router";
import SEO_CONSTANTS from "./Components/SEO/constants";

import './App.css';

function App() {
  return (
      <>
        <HelmetProvider>
          <Helmet>
              <title>{SEO_CONSTANTS.home.title}</title>
              <meta name="og:title" content={SEO_CONSTANTS.home.title} />
              <meta name="og:description" content={SEO_CONSTANTS.home.title} />

              <meta name="description" content={SEO_CONSTANTS.home.description} />
              <meta name="og:description" content={SEO_CONSTANTS.home.description} />
              <meta name="twitter:description" content={SEO_CONSTANTS.home.description} />

              <meta property="og:url" content={`${window.location.href}`} />
          </Helmet>
        </HelmetProvider>

        <Router />
      </>
  );
}

export default App;
