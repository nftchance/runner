import { HelmetProvider, Helmet } from "react-helmet-async";


import { library } from "@fortawesome/fontawesome-svg-core"
import { fab } from "@fortawesome/free-brands-svg-icons"
import { fal } from "@fortawesome/pro-light-svg-icons"

import Router from "@components/Router/Router";
import { SEO_CONSTANTS } from "@components/Constants/constants";

import "./App.css";

library.add(fab, fal)

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
