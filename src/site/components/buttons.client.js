'use client';
import React from 'react';
import Link from 'next/link';


export const LinkButton = ({ href, children }) => (
    <Link href={href}>
        <p style={{ padding: '10px', fontSize: '16px', textDecoration: 'none', color: 'black' }}>
            {children}
        </p>
    </Link>
);

export const FuncButton = ({ funcName, params, children }) => {
    const handleClick = async () => {
        // Construct the URL of the Flask route
        const url = `http://localhost:5000/summary`;

        // Make the HTTP request and log the response
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ funcName, params })
        });
        const data = await response.json();
        console.log(data);
    };

    return (
        <button onClick={handleClick} style={{ padding: '10px', fontSize: '16px' }}>
            {children}
        </button>
    );
};