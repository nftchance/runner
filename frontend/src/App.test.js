import React from "react";
import ReactDOM from "react-dom/client";
import {render, fireEvent, waitFor, screen} from '@testing-library/react'

import '@testing-library/jest-dom'

let container;

beforeEach(() => {
  container = document.createElement('div');
  document.body.appendChild(container);
});

afterEach(() => {
  document.body.removeChild(container);
  container = null;
});

import App from "./App"
it('can render App', async () => {
  await waitFor(() => { 
    ReactDOM.createRoot(container).render(<App />)
  });
});

import Home from "@components/Home/Home"
it('can render Home', async () => {
  await waitFor(() => { 
    ReactDOM.createRoot(container).render(<Home />)
  });
});


import Roadmap from "@components/Roadmap/Roadmap"
it('can render Roadmap', async () => {
  await waitFor(() => { 
    ReactDOM.createRoot(container).render(<Roadmap />)
  });
});

import FAQ from "@components/FAQ/FAQ"
it('can render FAQ', async () => {
  await waitFor(() => { 
    ReactDOM.createRoot(container).render(<FAQ />)
  });
});

import Governance from "@components/Governance/Governance"
it('can render Governance', async () => {
  await waitFor(() => { 
    ReactDOM.createRoot(container).render(<Governance />)
  });
});

import Proposal from "@components/Governance/Proposal"
it('can render Proposal', async () => {
  await waitFor(() => { 
    ReactDOM.createRoot(container).render(<Proposal />)
  });
});