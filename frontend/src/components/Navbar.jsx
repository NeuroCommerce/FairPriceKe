import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { FaXmark, FaBars } from "react-icons/fa6";

const Navbar = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [isSticky, setIsSticky] = useState(false);

    // Toggle menu
    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    }

    // Sticky navbar
    useEffect(() => {
        const handleScroll = () => {
            if (window.scrollY > 100) {
                setIsSticky(true);
            } else {
                setIsSticky(false);
            }
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    // navItems array
    const navItems = [
        { link: 'Home', path: '/home' },
        { link: 'About', path: '/about' },
        { link: 'Services', path: '/services' },
        { link: 'Contact', path: '/contact' },
    ];

    return (
        <header className='w-full bg-white md:bg-transparent fixed top-0 left-0 right-0'>
            <nav className={`py-4 lg:px-14 px-4 ${isSticky ? "sticky top-0 left-0 right-0 border-b bg-white duration-300" : ""}`}>
                <div className='flex justify-between items-center text-base gap-8'>
                    <h1 className='text-4xl font-bold'>Fair<span className='text-blue'>Price</span></h1>

                    {/* nav items for large devices */}
                    <ul className='md:flex space-x-12 hidden'>
                        {navItems.map(({ link, path }) => (
                            <li key={path}>
                                <Link to={path} className='block text-base text-gray-900 hover:text-blue first:font-medium'>
                                    {link}
                                </Link>
                            </li>
                        ))}
                    </ul>

                    {/* btn for large devices */}
                    <div className='space-x-12 hidden lg:flex items-center'>
                        <a href="/" className='text-blue hover:text-gray-800'>Login</a>
                        <button className='px-4 py-2 text-white rounded transition-all bg-blue hover:bg-gray-600 hover:text-gray-800'>Sign up</button>
                    </div>

                    {/* menu btn for only small devices */}
                    <div className='md:hidden'>
                        <button 
                            onClick={toggleMenu}
                            className='focus:outline-none text-gray-600 focus:text-gray-600'>
                            {
                                isMenuOpen ? (<FaXmark className='h-6 w-6 text-blue' />) : (<FaBars className='h-6 w-6' />)
                            }
                        </button>
                    </div>
                </div>

                {/* nav items for mobile */}
                <div className={`space-y-4 px-4 mt-16 py-7 bg-blue ${isMenuOpen ? "block fixed top-0 right-0 left-0" : "hidden"}`}>
                    {/* Navigation links */}
                    {
                        navItems.map(({ link, path }) => (
                            <Link 
                                to={path} 
                                key={path} 
                                className='block text-base text-gray-900 hover:text-white first:font-medium'
                                onClick={() => setIsMenuOpen(false)}  // Close menu after clicking link
                            >
                                {link}
                            </Link>
                        ))
                    }

                    {/* Login and Sign Up buttons for mobile */}
                    <div className="flex flex-col space-y-4 mt-8">
                        <a href="/" className='block text-white text-center py-2 px-4 rounded bg-gray-800 hover:bg-gray-900'>Login</a>
                        <button className='block py-2 px-4 rounded bg-white text-blue hover:bg-gray-100 hover:text-gray-800'>
                            Sign up
                        </button>
                    </div>
                </div>
            </nav>
        </header>
    );
}

export default Navbar;
