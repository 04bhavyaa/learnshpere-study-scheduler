import React from "react";

import "./Navbar.css";
import Image from "next/image";
import Link from "next/link";

export default function Navbar() {
    return (
        <div className="nav-container">
            <div className="navbar1">
                <div className="logo">
                    <Image
                        src="/Logo_3.png"
                        width={90}
                        height={90}
                        alt="logo"
                    />
                </div>

                <div className="links-container">
                    <div className="links">
                        <Link href={'/'}>Home</Link>
                        <Link href={"/About"}>About</Link>
                        <Link href={'/Contact'}>Contact</Link>
                    </div>
                </div>

                <Link href={"/Feature"}><button className="button-33" role="button">Dashboard</button></Link>
            </div>
        </div>
    )
}