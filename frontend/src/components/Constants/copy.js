import { URL_CONSTANTS } from "./constants"

import badge from "@images/badge.png"
import quickbooks from "@images/providers/quickbooks.png"
import twilio from "@images/providers/twilio.svg"
import mandrill from "@images/providers/mandrill.png"
import google from "@images/providers/google.png"

export const SYSTEM_MESSAGE = {
    message: 'Runner is currently in Beta | Read the latest article',
    linkTo: 'https://www.medium.com'
}

export const LANDING_CATEGORIES = [
    {
        title: 'Jobs', 
        description: 'The driving force of all service businesses, jobs are the blood of every business.',
        icon: ['fal', 'briefcase'],
        link: '/'
    },
    {
        title: 'Teams', 
        description: 'No job can be completed without a team! Every team is different though and you have control of every detail.',
        icon: ['fal', 'people-group'],
        link: '/'
    },
    {
        title: 'Customers', 
        description: 'Customer experience is the end-all and Runner focuses on assisting to deliver the best experience possible.',
        icon: ['fal', 'hand-holding-dollar'],
        link: '/'
    },
    {
        title: 'Tasks', 
        description: 'Unshackle you and your businesses from the never ending of side-tasks with impact-focused automation.',
        icon: ['fal', 'check'],
        link: '/'
    },
]

export const LANDING_MODULES = [
    {
        title: 'Managed Team Scheduling',
        description: 'Stay ahead of the curve by utilizing historical data to predict the future. Enabling more efficient team dispatching, your business can do more in less time.',
        provider: 'runner',
        providerLogo: badge,
        linkTo: '/'
    },
    {
        title: 'Payroll Streaming',
        description: 'The all-in-one notification kit for all Job updates. Instantly update the client, the team assigned, and management without a single manual action.',
        provider: 'QuickBooks',
        providerLogo: quickbooks,
        linkTo: '/'
    },
    {
        title: 'Real-Time KP Reports',
        description: 'Gain access to the key stats of your service business without the need to do any tracking or math yourself. Import, export, analyze and plan. All in one place.',
        provider: 'runner',
        providerLogo: badge,
        linkTo: '/'
    },
    {
        title: 'Job Notifications',
        description: 'The all-in-one notification kit for all Job updates. Instantly update the client, the team assigned, and management without a single manual action.',
        provider: 'Twilio',
        providerLogo: twilio,
        linkTo: '/'
    },
    {
        title: 'Transactional Emails',
        description: 'The all-in-one notification kit for all Job updates. Instantly update the client, the team assigned, and management without a single manual action.',
        provider: 'Mandrill',
        providerLogo: mandrill,
        linkTo: '/'
    },
    {
        title: 'Mileage Tracking',
        description: 'The all-in-one notification kit for all Job updates. Instantly update the client, the team assigned, and management without a single manual action.',
        provider: 'Google',
        providerLogo: google,
        linkTo: '/'
    },
]

export const FOOTER_ITEMS = [
    {
        name: 'Product', 
        items: [
            {
                title: 'Organizations',
                link: '/organizations',
                external: false
            },
            {
                title: 'Jobs',
                link: '/jobs',
                external: false
            },
            {
                title: 'Teams',
                link: '/teams',
                external: false
            },
            {
                title: 'Task Automation',
                link: '/task-automation',
                external: false
            },
            {
                title: 'Pricing',
                link: '/pricing',
                external: false
            },
        ]
    },
    {
        name: 'Resources',
        items: [
            {
                title: 'Community',
                link: '/community',
                external: false
            },
            {
                title: 'Brand Assets',
                link: '/brand',
                external: false
            },
            {
                title: 'Integrations',
                link: '/integrations',
                external: false
            },
            {
                title: 'System Status',
                link: '/system-status',
                external: false
            },
            {
                title: 'Support',
                link: '/support',
                external: false
            },
        ]
    },
    {
        name: 'Developers',
        items: [
            {
                title: 'Documentation',
                link: '/docs',
                external: false
            },
            {
                title: 'API Reference',
                link: '/docs/api',
                external: false
            },
            {
                title: 'Guides',
                link: '/guides',
                external: false
            },
            {
                title: 'Pre-Built Plugins',
                link: '/plugins',
                external: false
            },
        ]
    },
    {
        name: 'Company',
        items: [
            {
                title: 'Open Source',
                link: URL_CONSTANTS.github,
                external: true
            },
            {
                title: 'Terms of Service',
                link: '/terms-of-service',
                external: false
            },
            {
                title: 'Privacy Policy',
                link: '/privacy-policy',
                external: false
            },
        ]
    }
]

export const LANDING_DASHBOARD_TABS = [
    {
        tab: 'Organization',
        title: 'This is placeholder organization text',
        description: "Organization placeholder description lorem ipsum dolor lorem ipsum dolor lorem ipsum dolor lorem ipsum dolor.",
        buttonText: 'Explore Organization Metrics',
        linkTo: '/'
    },
    {
        tab: 'Services',
        title: 'Placeholder Services text',
        description: "Services placeholder text lorem ipsum dolor lorem ipsum dolor lorem ipsum dolor lorem ipsum dolor lorem ipsum.",
        buttonText: 'Explore Service Actions',
        linkTo: '/'
    },
    {
        tab: 'Maintenance',
        title: 'Watch as each piece of maintenance is handled automatically',
        description: "You don't have to be a super computer to manage every piece of your service business. Our system makes every piece of business leadership easy by automating the tasks that don't need manager oversight.",
        buttonText: 'Explore Maintenance Actions',
        linkTo: '/'
    },
]

export const ROADMAP_TASKS = [
    {
        version: 'V0.1',
        description: 'Focusing on foundational layers, v0.1 introduces the core function systems of the Runner system.',
        tasks: [
            {
                title: 'Global Account Systems',
                description: 'Implement the core of authentication, Runner is built on an open-user approach that allows quick transition through organizations.',
                status: 'In Progress',
                statusIndicatorColor: 'green',
                linkTo: '/'
            },
            {
                title: 'Asynchronous Feeds',
                description: 'One of the least efficient aspects of service businesses are the sequential nature of task completion. Async operation redefines that.',
                status: 'Upcoming',
                statusIndicatorColor: 'light-blue',
                linkTo: '/'
            },
            {
                title: 'Scheduled Instances',
                description: 'Compounding on top of atomic data, the seamless operation of time and state level triggers are key to custom workflows.',
                status: 'Upcoming',
                statusIndicatorColor: 'light-blue',
                linkTo: '/'
            },
            {
                title: 'Mobile-First Front-End',
                description: 'With the majority of services being render in-field, the user-experience is key to securing the highest level of impact from the utilization of better tools.',
                status: 'Upcoming',
                statusIndicatorColor: 'light-blue',
                linkTo: '/'
            },
            {
                title: 'Global Account Systems',
                description: 'Implement the core of authentication, Runner is built on an open-user approach that allows quick transition through organizations.',
                status: 'Upcoming',
                statusIndicatorColor: 'light-blue',
                linkTo: '/'
            },
            {
                title: 'Asynchronous Feeds',
                description: 'One of the least efficient aspects of service businesses are the sequential nature of task completion. Async operation redefines that.',
                status: 'Upcoming',
                statusIndicatorColor: 'light-blue',
                linkTo: '/'
            },
        ]
    },
    {
        version: 'V0.2',
        description: 'In quick succession of releases, this version is planned to introduce the underlying automation framework.',
        tasks: [
            {
                title: 'Global Account Systems',
                description: 'Implement the core of authentication, Runner is built on an open-user approach that allows quick transition through organizations.',
                status: 'Upcoming',
                statusIndicatorColor: 'light-blue',
                linkTo: '/'
            },
            {
                title: 'Asynchronous Feeds',
                description: 'One of the least efficient aspects of service businesses are the sequential nature of task completion. Async operation redefines that.',
                status: 'Upcoming',
                statusIndicatorColor: 'light-blue',
                linkTo: '/'
            },
            {
                title: 'Scheduled Instances',
                description: 'Compounding on top of atomic data, the seamless operation of time and state level triggers are key to custom workflows.',
                status: 'Upcoming',
                statusIndicatorColor: 'light-blue',
                linkTo: '/'
            },
        ]
    },
    {
        version: 'V0.3',
        description: 'With the skeleton of Runner in place, this update hones in on the automation of long-tail management mechanisms.',
        tasks: [
            {
                title: 'Payroll Streaming',
                description: 'Compounding on top of atomic data, the seamless operation of time and state level triggers are key to custom workflows.',
                status: 'Upcoming',
                statusIndicatorColor: 'light-blue',
                linkTo: '/'
            },
            {
                title: 'Team Scheduling',
                description: 'Compounding on top of atomic data, the seamless operation of time and state level triggers are key to custom workflows.',
                status: 'Upcoming',
                statusIndicatorColor: 'light-blue',
                linkTo: '/'
            },
            {
                title: 'Plug-In System',
                description: 'Compounding on top of atomic data, the seamless operation of time and state level triggers are key to custom workflows.',
                status: 'Upcoming',
                statusIndicatorColor: 'light-blue',
                linkTo: '/'
            },
            {
                title: 'Platform Governance',
                description: 'Compounding on top of atomic data, the seamless operation of time and state level triggers are key to custom workflows.',
                status: 'Upcoming',
                statusIndicatorColor: 'light-blue',
                linkTo: '/'
            },
        ]
    },
]

export const FAQ_ITEMS = [
    {
        question: 'How can my business benefit from runner?',
        answer: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus luctus felis accumsan nibh fermentum facilisis. Sed facilisis facilisis nulla, a tempor turpis aliquam sed. Fusce elit ante, fermentum vulputate fermentum ut, porttitor a magna. Ut quis dictum felis. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aenean non lobortis quam. Vivamus semper facilisis quam, vel pharetra massa mollis eget. Donec rhoncus aliquam blandit. Nullam ut feugiat elit. Aliquam finibus vestibulum arcu, vitae interdum ante accumsan quis. Integer id feugiat arcu. Fusce id sem quis nunc egestas condimentum id quis nunc. Pellentesque leo nisl, facilisis non augue nec, sollicitudin euismod justo. \n\nMorbi leo magna, lobortis at aliquet interdum, pellentesque nec quam. Cras vestibulum est non ex accumsan luctus. Proin fermentum risus eget pretium blandit. Phasellus ornare accumsan odio ut auctor. Suspendisse eu mattis lorem, at interdum quam. Maecenas finibus molestie egestas. Sed eu orci tempus, volutpat est et, luctus nisi. Nulla nunc mi, tristique non ex eget, tincidunt aliquam sapien.',
    },
    {
        question: 'What are the downsides of using runner for my service business?',
        answer: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus luctus felis accumsan nibh fermentum facilisis. Sed facilisis facilisis nulla, a tempor turpis aliquam sed. Fusce elit ante, fermentum vulputate fermentum ut, porttitor a magna. Ut quis dictum felis. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aenean non lobortis quam. Vivamus semper facilisis quam, vel pharetra massa mollis eget. Donec rhoncus aliquam blandit. Nullam ut feugiat elit. Aliquam finibus vestibulum arcu, vitae interdum ante accumsan quis. Integer id feugiat arcu. Fusce id sem quis nunc egestas condimentum id quis nunc. Pellentesque leo nisl, facilisis non augue nec, sollicitudin euismod justo. \n\nMorbi leo magna, lobortis at aliquet interdum, pellentesque nec quam. Cras vestibulum est non ex accumsan luctus. Proin fermentum risus eget pretium blandit. Phasellus ornare accumsan odio ut auctor. Suspendisse eu mattis lorem, at interdum quam. Maecenas finibus molestie egestas. Sed eu orci tempus, volutpat est et, luctus nisi. Nulla nunc mi, tristique non ex eget, tincidunt aliquam sapien.',
    },
    {
        question: 'Will runner work for any service industry?',
        answer: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus luctus felis accumsan nibh fermentum facilisis. Sed facilisis facilisis nulla, a tempor turpis aliquam sed. Fusce elit ante, fermentum vulputate fermentum ut, porttitor a magna. Ut quis dictum felis. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aenean non lobortis quam. Vivamus semper facilisis quam, vel pharetra massa mollis eget. Donec rhoncus aliquam blandit. Nullam ut feugiat elit. Aliquam finibus vestibulum arcu, vitae interdum ante accumsan quis. Integer id feugiat arcu. Fusce id sem quis nunc egestas condimentum id quis nunc. Pellentesque leo nisl, facilisis non augue nec, sollicitudin euismod justo. \n\nMorbi leo magna, lobortis at aliquet interdum, pellentesque nec quam. Cras vestibulum est non ex accumsan luctus. Proin fermentum risus eget pretium blandit. Phasellus ornare accumsan odio ut auctor. Suspendisse eu mattis lorem, at interdum quam. Maecenas finibus molestie egestas. Sed eu orci tempus, volutpat est et, luctus nisi. Nulla nunc mi, tristique non ex eget, tincidunt aliquam sapien.',
    },
    {
        question: 'How does runner make money if I can use the service for free?',
        answer: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus luctus felis accumsan nibh fermentum facilisis. Sed facilisis facilisis nulla, a tempor turpis aliquam sed. Fusce elit ante, fermentum vulputate fermentum ut, porttitor a magna. Ut quis dictum felis. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aenean non lobortis quam. Vivamus semper facilisis quam, vel pharetra massa mollis eget. Donec rhoncus aliquam blandit. Nullam ut feugiat elit. Aliquam finibus vestibulum arcu, vitae interdum ante accumsan quis. Integer id feugiat arcu. Fusce id sem quis nunc egestas condimentum id quis nunc. Pellentesque leo nisl, facilisis non augue nec, sollicitudin euismod justo. \n\nMorbi leo magna, lobortis at aliquet interdum, pellentesque nec quam. Cras vestibulum est non ex accumsan luctus. Proin fermentum risus eget pretium blandit. Phasellus ornare accumsan odio ut auctor. Suspendisse eu mattis lorem, at interdum quam. Maecenas finibus molestie egestas. Sed eu orci tempus, volutpat est et, luctus nisi. Nulla nunc mi, tristique non ex eget, tincidunt aliquam sapien.',
    },
    {
        question: `What does 'governance' mean and how do I get involved?`,
        answer: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus luctus felis accumsan nibh fermentum facilisis. Sed facilisis facilisis nulla, a tempor turpis aliquam sed. Fusce elit ante, fermentum vulputate fermentum ut, porttitor a magna. Ut quis dictum felis. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aenean non lobortis quam. Vivamus semper facilisis quam, vel pharetra massa mollis eget. Donec rhoncus aliquam blandit. Nullam ut feugiat elit. Aliquam finibus vestibulum arcu, vitae interdum ante accumsan quis. Integer id feugiat arcu. Fusce id sem quis nunc egestas condimentum id quis nunc. Pellentesque leo nisl, facilisis non augue nec, sollicitudin euismod justo. \n\nMorbi leo magna, lobortis at aliquet interdum, pellentesque nec quam. Cras vestibulum est non ex accumsan luctus. Proin fermentum risus eget pretium blandit. Phasellus ornare accumsan odio ut auctor. Suspendisse eu mattis lorem, at interdum quam. Maecenas finibus molestie egestas. Sed eu orci tempus, volutpat est et, luctus nisi. Nulla nunc mi, tristique non ex eget, tincidunt aliquam sapien.',
    },
    {
        question: 'Can I get a demo of how runner is used for a service business?',
        answer: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus luctus felis accumsan nibh fermentum facilisis. Sed facilisis facilisis nulla, a tempor turpis aliquam sed. Fusce elit ante, fermentum vulputate fermentum ut, porttitor a magna. Ut quis dictum felis. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aenean non lobortis quam. Vivamus semper facilisis quam, vel pharetra massa mollis eget. Donec rhoncus aliquam blandit. Nullam ut feugiat elit. Aliquam finibus vestibulum arcu, vitae interdum ante accumsan quis. Integer id feugiat arcu. Fusce id sem quis nunc egestas condimentum id quis nunc. Pellentesque leo nisl, facilisis non augue nec, sollicitudin euismod justo. \n\nMorbi leo magna, lobortis at aliquet interdum, pellentesque nec quam. Cras vestibulum est non ex accumsan luctus. Proin fermentum risus eget pretium blandit. Phasellus ornare accumsan odio ut auctor. Suspendisse eu mattis lorem, at interdum quam. Maecenas finibus molestie egestas. Sed eu orci tempus, volutpat est et, luctus nisi. Nulla nunc mi, tristique non ex eget, tincidunt aliquam sapien.',
    },
    {
        question: 'What do I need to do to migrate to using runner?',
        answer: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus luctus felis accumsan nibh fermentum facilisis. Sed facilisis facilisis nulla, a tempor turpis aliquam sed. Fusce elit ante, fermentum vulputate fermentum ut, porttitor a magna. Ut quis dictum felis. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aenean non lobortis quam. Vivamus semper facilisis quam, vel pharetra massa mollis eget. Donec rhoncus aliquam blandit. Nullam ut feugiat elit. Aliquam finibus vestibulum arcu, vitae interdum ante accumsan quis. Integer id feugiat arcu. Fusce id sem quis nunc egestas condimentum id quis nunc. Pellentesque leo nisl, facilisis non augue nec, sollicitudin euismod justo. \n\nMorbi leo magna, lobortis at aliquet interdum, pellentesque nec quam. Cras vestibulum est non ex accumsan luctus. Proin fermentum risus eget pretium blandit. Phasellus ornare accumsan odio ut auctor. Suspendisse eu mattis lorem, at interdum quam. Maecenas finibus molestie egestas. Sed eu orci tempus, volutpat est et, luctus nisi. Nulla nunc mi, tristique non ex eget, tincidunt aliquam sapien.',
    },
    {
        question: 'Is there a plug-and-play solution for runner? / Do I need to be technical to use runner?',
        answer: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus luctus felis accumsan nibh fermentum facilisis. Sed facilisis facilisis nulla, a tempor turpis aliquam sed. Fusce elit ante, fermentum vulputate fermentum ut, porttitor a magna. Ut quis dictum felis. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aenean non lobortis quam. Vivamus semper facilisis quam, vel pharetra massa mollis eget. Donec rhoncus aliquam blandit. Nullam ut feugiat elit. Aliquam finibus vestibulum arcu, vitae interdum ante accumsan quis. Integer id feugiat arcu. Fusce id sem quis nunc egestas condimentum id quis nunc. Pellentesque leo nisl, facilisis non augue nec, sollicitudin euismod justo. \n\nMorbi leo magna, lobortis at aliquet interdum, pellentesque nec quam. Cras vestibulum est non ex accumsan luctus. Proin fermentum risus eget pretium blandit. Phasellus ornare accumsan odio ut auctor. Suspendisse eu mattis lorem, at interdum quam. Maecenas finibus molestie egestas. Sed eu orci tempus, volutpat est et, luctus nisi. Nulla nunc mi, tristique non ex eget, tincidunt aliquam sapien.',
    },
]

export const PROPOSAL_DATA = [
    {
        title: '[RP1] Mobile-First Front-End',
        description: 'With the majority of services being render in-field, the user-experience is key to securing the highest level of impact from the utilization of better tools.',
        tags: [
            'Dashboard',
            'UX'
        ], 
        votingPercents: [60, 25],
        linkTo: '/'
    },
    {
        title: '[RP2] Sales Tax Integration',
        description: 'With the majority of services being render in-field, the user-experience is key to securing the highest level of impact from the utilization of better tools.',
        tags: [
            'Financials',
            'Taxes'
        ], 
        votingPercents: [92, 0],
        linkTo: '/'
    },
    {
        title: '[RP3] Yelp Integration',
        description: 'With the majority of services being render in-field, the user-experience is key to securing the highest level of impact from the utilization of better tools.',
        tags: [
            'Reviews'
        ], 
        votingPercents: [5, 80],
        linkTo: '/'
    },
    {
        title: '[RP4] Mobile App Notifications',
        description: 'With the majority of services being render in-field, the user-experience is key to securing the highest level of impact from the utilization of better tools.',
        tags: [
            'Mobile',
            'UX'
        ], 
        votingPercents: [15, 10],
        linkTo: '/'
    },
    {
        title: '[RP5] Cancellation Fees',
        description: 'With the majority of services being render in-field, the user-experience is key to securing the highest level of impact from the utilization of better tools.',
        tags: [
            'Financials',
            'Fees'
        ], 
        votingPercents: [25, 5],
        linkTo: '/'
    },
    {
        title: '[RP6] Usage Based Payments',
        description: 'With the majority of services being render in-field, the user-experience is key to securing the highest level of impact from the utilization of better tools.',
        tags: [
            'Financials',
            'Payments'
        ], 
        votingPercents: [5, 10],
        linkTo: '/'
    },
    {
        title: '[RP7] Invoice Management',
        description: 'With the majority of services being render in-field, the user-experience is key to securing the highest level of impact from the utilization of better tools.',
        tags: [
            'Dashboard',
            'Integrations',
            'Payments'
        ], 
        votingPercents: [55, 30],
        linkTo: '/'
    },
    {
        title: '[RP8] Zapier Integration',
        description: 'With the majority of services being render in-field, the user-experience is key to securing the highest level of impact from the utilization of better tools.',
        tags: [
            'Integrations'
        ], 
        votingPercents: [80, 10],
        linkTo: '/'
    },
]

export const VOLUME_BARS = [
    {
        height: "0px",
        volume: "$0.00",
        runner: "0 $RUNNER"
    },
    {
        height: "3px",
        volume: "$805.56",
        runner: "4 $RUNNER"
    },
    {
        height: "5px",
        volume: "$1,611.11",
        runner: "10 $RUNNER"
    },
    {
        height: "6px",
        volume: "$2,416.67",
        runner: "17 $RUNNER"
    },
    {
        height: "7px",
        volume: "$3,222.22",
        runner: "24 $RUNNER"
    },
    {
        height: "8px",
        volume: "$4,027.78",
        runner: "32 $RUNNER"
    },
    {
        height: "9px",
        volume: "$4,833.33",
        runner: "40 $RUNNER"
    },
    {
        height: "11px",
        volume: "$5,638.89",
        runner: "49 $RUNNER"
    },
    {
        height: "12px",
        volume: "$6,444.44",
        runner: "58 $RUNNER"
    },
    {
        height: "15px",
        volume: "$7,250.00",
        runner: "67 $RUNNER"
    },
    {
        height: "20px",
        volume: "$8,055.56",
        runner: "76 $RUNNER"
    },
    {
        height: "24px",
        volume: "$8,861.11",
        runner: "86 $RUNNER"
    },
    {
        height: "33px",
        volume: "$9,666.67",
        runner: "96 $RUNNER"
    },
    {
        height: "42px",
        volume: "$10,472.22",
        runner: "106 $RUNNER"
    },
    {
        height: "50px",
        volume: "$11,277.78",
        runner: "116 $RUNNER"
    },
    {
        height: "59px",
        volume: "$12,083.33",
        runner: "127 $RUNNER"
    },
    {
        height: "68px",
        volume: "$12,888.89",
        runner: "137 $RUNNER"
    },
    {
        height: "82px",
        volume: "$13,694.44",
        runner: "148 $RUNNER"
    },
    {
        height: "91px",
        volume: "$14,500.00",
        runner: "159 $RUNNER"
    },
    {
        height: "108px",
        volume: "$15,305.56",
        runner: "170 $RUNNER"
    },
    {
        height: "123px",
        volume: "$16,111.11",
        runner: "182 $RUNNER"
    },
    {
        height: "138px",
        volume: "$16,916.67",
        runner: "193 $RUNNER"
    },
    {
        height: "158px",
        volume: "$17,722.22",
        runner: "204 $RUNNER"
    },
    {
        height: "180px",
        volume: "$18,527.78",
        runner: "216 $RUNNER"
    },
    {
        height: "204px",
        volume: "$19,333.33",
        runner: "228 $RUNNER"
    },
    {
        height: "226px",
        volume: "$20,138.89",
        runner: "240 $RUNNER"
    },
    {
        height: "254px",
        volume: "$20,944.44",
        runner: "252 $RUNNER"
    },
    {
        height: "278px",
        volume: "$21,750.00",
        runner: "264 $RUNNER"
    },
]