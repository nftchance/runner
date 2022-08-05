import "./Page.css";

import Navbar from "@components/Navbar/Navbar";
import Footer from "@components/Footer/Footer";
import SystemMessage from "@components/SystemMessage/SystemMessage";

const Page = ({children}) => {
    const message = "Runner is currently in Beta | Read the latest article";
    const directTo = "https://www.medium.com"

    return (
        <>
            <SystemMessage message={message} directTo={directTo} />

            <Navbar />

            <div className="page-margin">
                {children}
            </div>

            <Footer />
        </>
    )
}

export default Page;