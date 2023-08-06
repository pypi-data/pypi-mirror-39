__all__ = ('example_keypair', )


example_keypair = [
    (
        'keypairs',
        [
            {
                # Admin user example key
                'user_id': 'admin@lablup.com',
                'access_key': 'AKIAIOSFODNN7EXAMPLE',
                'secret_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                'is_active': True,
                'billing_plan': 'free',
                'concurrency_limit': 30,
                'concurrency_used': 0,
                'rate_limit': 1000,
                'num_queries': 0,
                'is_admin': True,
            },
            {
                # Non-admin user example key
                'user_id': 'user@lablup.com',
                'access_key': 'AKIANABBDUSEREXAMPLE',
                'secret_key': 'C8qnIo29EZvXkPK_MXcuAakYTy4NYrxwmCEyNPlf',
                'is_active': True,
                'billing_plan': 'free',
                'concurrency_limit': 30,
                'concurrency_used': 0,
                'rate_limit': 1000,
                'num_queries': 0,
                'is_admin': False,
            },
        ]
    ),
]
