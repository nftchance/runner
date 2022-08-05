export const SEO_CONSTANTS = {
    home: {
        title: "runner",
        description: "Revolutionize your service business with automation tools of 2032."
    }
}

export const URL_CONSTANTS = {
    discord: "http://discord.com",
    twitter: "http://twitter.com",
    github: "https://github.com/nftchance/runner"
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
        providerLogo: '/badge.svg'
    },
    {
        title: 'Payroll Streaming',
        description: 'The all-in-one notification kit for all Job updates. Instantly update the client, the team assigned, and management without a single manual action.',
        provider: 'QuickBooks',
        providerLogo: '/badge.svg'
    },
    {
        title: 'Real-Time KP Reports',
        description: 'Gain access to the key stats of your service business without the need to do any tracking or math yourself. Import, export, analyze and plan. All in one place.',
        provider: 'runner',
        providerLogo: '/badge.svg'
    },
    {
        title: 'Job Notifications',
        description: 'The all-in-one notification kit for all Job updates. Instantly update the client, the team assigned, and management without a single manual action.',
        provider: 'Twilio',
        providerLogo: '/badge.svg'
    },
    {
        title: 'Transactional Emails',
        description: 'The all-in-one notification kit for all Job updates. Instantly update the client, the team assigned, and management without a single manual action.',
        provider: 'Mandrill',
        providerLogo: '/badge.svg'
    },
    {
        title: 'Mileage Tracking',
        description: 'The all-in-one notification kit for all Job updates. Instantly update the client, the team assigned, and management without a single manual action.',
        provider: 'Google',
        providerLogo: '/badge.svg'
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