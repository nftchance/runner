import "./Footer.css"
import {useEffect} from 'react'

const Footer = () => {
    const links = [
        {
            Product: [
                {
                    'title': 'Organizations',
                    'link': '/organizations'
                },
                {
                    'title': 'Jobs',
                    'link': '/jobs'
                },
                {
                    'title': 'Teams',
                    'link': '/teams'
                },
                {
                    'title': 'Task Automation',
                    'link': '/task-automation'
                },
                {
                    'title': 'Pricing',
                    'link': '/pricing'
                },
            ]
        },
        {
            Resources: [
                {
                    'title': 'Jobs',
                    'link': '/jobs'
                },
                {
                    'title': 'Jobs',
                    'link': '/jobs'
                },
                {
                    'title': 'Jobs',
                    'link': '/jobs'
                },
                {
                    'title': 'Jobs',
                    'link': '/jobs'
                },
                {
                    'title': 'Jobs',
                    'link': '/jobs'
                },
            ]
        },
        {
            Developers: [
                {
                    'title': 'Jobs',
                    'link': '/jobs'
                },
                {
                    'title': 'Jobs',
                    'link': '/jobs'
                },
                {
                    'title': 'Jobs',
                    'link': '/jobs'
                },
                {
                    'title': 'Jobs',
                    'link': '/jobs'
                },
            ]
        },
        {
            Company: [
                {
                    'title': 'Jobs',
                    'link': '/jobs'
                },
                {
                    'title': 'Jobs',
                    'link': '/jobs'
                },
                {
                    'title': 'Jobs',
                    'link': '/jobs'
                },
            ]
        }
    ]

    const data = () => {
        links.forEach((category) => {
            console.log('Category', Object.keys(category))
            console.log('Items', Object.values(category))
            Object.values(category)[0].forEach((index, item) => {
                console.log('index', index)
                console.log(item)
            })
        })
    }

    useEffect(() => {
        data()
    }, [])

    return (
        <div className="footer">
            <div className="grid">
                <div className="social-icons">

                </div>

                {links.map((category) => (
                    <ul key={`${Object.keys(category)}`}>
                        <li>
                            <h5>{Object.keys(category)}</h5>
                        </li>
                        {Object.values(category)[0].map((item) => (
                            <li key={`${item.title}`}>
                                <a>
                                    <p>{item.title}</p>
                                </a>
                            </li>
                        ))}
                    </ul>
                ))}
            </div>

            <div className="footer-appendage">
                <p>©️ Runner Inc</p>
            </div>
        </div>
    )
}

export default Footer;