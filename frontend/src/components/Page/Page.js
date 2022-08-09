import "./Page.css";

import Navbar from "@components/Navbar/Navbar";
import Footer from "@components/Footer/Footer";
import SystemMessage from "@components/SystemMessage/SystemMessage";

import { SYSTEM_MESSAGE } from "@components/Constants/copy";

const Page = ({children}) => {
    return (
        <>
            <SystemMessage 
                message={SYSTEM_MESSAGE.message} 
                linkTo={SYSTEM_MESSAGE.linkTo} 
            />

            <Navbar />

            <div className="page-margin">
                {children}
            </div>

            <Footer />
        </>
    )
}

export default Page;