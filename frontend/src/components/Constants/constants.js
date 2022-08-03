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
        Product: [
            {
                'title': 'Organizations',
                'link': '/organizations',
                'external': false
            },
            {
                'title': 'Jobs',
                'link': '/jobs',
                'external': false
            },
            {
                'title': 'Teams',
                'link': '/teams',
                'external': false
            },
            {
                'title': 'Task Automation',
                'link': '/task-automation',
                'external': false
            },
            {
                'title': 'Pricing',
                'link': '/pricing',
                'external': false
            },
        ]
    },
    {
        Resources: [
            {
                'title': 'Community',
                'link': '/community',
                'external': false
            },
            {
                'title': 'Brand Assets',
                'link': '/brand',
                'external': false
            },
            {
                'title': 'Integrations',
                'link': '/integrations',
                'external': false
            },
            {
                'title': 'System Status',
                'link': '/system-status',
                'external': false
            },
            {
                'title': 'Support',
                'link': '/support',
                'external': false
            },
        ]
    },
    {
        Developers: [
            {
                'title': 'Documentation',
                'link': '/docs',
                'external': false
            },
            {
                'title': 'API Reference',
                'link': '/docs/api',
                'external': false
            },
            {
                'title': 'Guides',
                'link': '/guides',
                'external': false
            },
            {
                'title': 'Pre-Built Plugins',
                'link': '/plugins',
                'external': false
            },
        ]
    },
    {
        Company: [
            {
                'title': 'Open Source',
                'link': URL_CONSTANTS.github,
                'external': true
            },
            {
                'title': 'Terms of Service',
                'link': '/terms-of-service',
                'external': false
            },
            {
                'title': 'Privacy Policy',
                'link': '/privacy-policy',
                'external': false
            },
        ]
    }
]