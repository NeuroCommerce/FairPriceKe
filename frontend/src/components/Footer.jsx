import React from 'react';

const Footer = () => {
  return (
    <footer className='bg-gray-800 text-white py-8'>
      <div className='max-w-screen-2xl mx-auto px-4 md:px-14'>
        <div className='grid grid-cols-1 md:grid-cols-4 gap-8'>
          {/* About Us Section */}
          <div>
            <h2 className='text-xl font-semibold mb-4'>About Us</h2>
            <p>
              We are a dedicated team of professionals committed to providing exceptional services and solutions. Our goal is to leverage technology to create innovative products that enhance the lives of our customers.
            </p>
          </div>

          {/* Quick Links Section */}
          <div>
            <h2 className='text-xl font-semibold mb-4'>Quick Links</h2>
            <ul>
              <li className='mb-2'><a href='./Home' className='hover:underline'>Home</a></li>
              <li className='mb-2'><a href='./Services' className='hover:underline'>Services</a></li>
              <li className='mb-2'><a href='./About' className='hover:underline'>About</a></li>
              <li className='mb-2'><a href='./Contact' className='hover:underline'>Contact</a></li>
            </ul>
          </div>

          {/* Contact Information Section */}
          <div>
            <h2 className='text-xl font-semibold mb-4'>Contact Information</h2>
            <p>Email: contact@ourcompany.com</p>
            <p>Phone: +254 704 148 827</p>
            <p>Address: 123 Main Street, Anytown, USA</p>
          </div>

          {/* Social Media Section */}
          {/* <div>
            <h2 className='text-xl font-semibold mb-4'>Follow Us</h2>
            <div className='flex space-x-4'>
              <a href='#' className='hover:text-gray-400'><i className='fab fa-facebook-f'></i></a>
              <a href='#' className='hover:text-gray-400'><i className='fab fa-twitter'></i></a>
              <a href='#' className='hover:text-gray-400'><i className='fab fa-instagram'></i></a>
              <a href='#' className='hover:text-gray-400'><i className='fab fa-linkedin-in'></i></a>
            </div>
          </div> */}
        </div>

        <div className='text-center mt-8'>
          <p>&copy; {new Date().getFullYear()} Our Company. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;