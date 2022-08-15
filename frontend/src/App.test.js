import ReactDOM from "react-dom/client";
import { act } from 'react-dom/test-utils';
import {render, fireEvent, waitFor, screen} from '@testing-library/react'
import '@testing-library/jest-dom'

// Honestly this might be a hot take but testing this shit is so much of a goddamn pain I have no clue why it is done.
// Unless you have some complicated functions or want to verify API requests this seems beyond pointless to struggle through.

import App from "./App"
it('can render App', async () => {
  await act(() => {
    render(<App />)
  })

  const navbadge = screen.getByTestId("nav-badge");
  expect(navbadge).toBeInTheDocument();
});

// let container;

// beforeEach(() => {
//   container = document.createElement('div');
//   document.body.appendChild(container);
// });

// afterEach(() => {
//   document.body.removeChild(container);
//   container = null;
// });

// import App from "./App"
// it('can render App', async () => {
//   await waitFor(() => { 
//     ReactDOM.createRoot(container).render(<App />)
//   });
// });

// import Home from "@components/Home/Home"
// it('can render Home', async () => {
//   await waitFor(() => { 
//     ReactDOM.createRoot(container).render(<Home />)
//   });
// });

// import Roadmap from "@components/Roadmap/Roadmap"
// it('can render Roadmap', async () => {
//   await waitFor(() => { 
//     ReactDOM.createRoot(container).render(<Roadmap />)
//   });
// });

// import FAQ from "@components/FAQ/FAQ"
// it('can render FAQ', async () => {
//   await waitFor(() => { 
//     ReactDOM.createRoot(container).render(<FAQ />)
//   });
// });

// import Governance from "@components/Governance/Governance"
// it('can render Governance', async () => {
//   await waitFor(() => { 
//     ReactDOM.createRoot(container).render(<Governance />)
//   });
// });

// import Proposal from "@components/Governance/Proposal"
// it('can render Proposal', async () => {
//   await waitFor(() => { 
//     ReactDOM.createRoot(container).render(<Proposal />)
//   });
// });


// let links = []

// import App from "./App"
// it('can render App', async () => {
//   await act(() => {
//     render(<App />);
//   })

//   links = screen.getElementsByClassName("nav-link")
//   console.log(links)
//   expect(screen.getByTestId("nav-badge")).toBeInTheDocument();
//   expect(screen.queryByTestId("hero-title")).toBeInTheDocument();
// });

// it('can render Home', async () => {
//   await act(() => {
//     fireEvent.click(links[0])
//   })
// });

// it('can render Home', async () => {
//   const history = createMemoryHistory();
//   history.push('/')

//   console.log(screen)

//   expect(screen.queryByTestId("hero-title")).toBeInTheDocument();
// });