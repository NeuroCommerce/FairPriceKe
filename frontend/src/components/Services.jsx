import React from 'react';
import Amazon from '../assets/Amazon.png';
import Aliexpress from '../assets/Aliexpress.png';
import ebay from '../assets/ebay.png';
import jumia from '../assets/jumia.png';
import kilimall from '../assets/kilimall.png';

const Services = () => {
  return (
    <div className='bg-neutral-100 md:px-14 px-4 py-16 max-w-screen-2xl mx-auto hover duration-800 hover:-translate-x-8'>
      <div className='text-center my-8'>
        <h1 className='text-4xl font-semibold mb-4 text-primary'>Our Services</h1>
        <p className='text-primary text-base mb-8 font-serif'>
          We offer a wide range of AI-powered features to help you shop smarter and save time. Our services are designed to provide you with the best shopping experience by leveraging advanced algorithms and machine learning techniques. Whether you are looking for personalized recommendations, price comparisons, or seamless checkout processes, we have got you covered.
        </p>

        {/* company logos */}
        <div className='my-12 flex-wrap flex justify-between items-center gap-8'>
          <img src={Amazon} alt='Amazon' className='w-16 h-16' />
          <img src={Aliexpress} alt='Aliexpress' className='w-16 h-16' />
          <img src={ebay} alt='ebay' className='w-16 h-16' />
          <img src={jumia} alt='Jumia' className='w-16 h-16' />
          <img src={kilimall} alt='Kilimall' className='w-16 h-16' />
        </div>
      </div>

      {/* Features Section */}
      <div className='my-16 text-center justify-between' >
        <h2 className='text-3xl font-bold mb-4 text-primary'>Features</h2>
        <ul className='font-serif pl-5'>
          <li className='mb-2'>- Personalized Recommendations: Get suggestions tailored to your preferences.</li>
          <li className='mb-2'>- Price Comparisons: Find the best deals across multiple platforms.</li>
          <li className='mb-2'>- Seamless Checkout: Enjoy a smooth and quick checkout process.</li>
        </ul>
      </div>

        {/* Benefits Section */}
        {/* <div className='my-16 text-center justify-between' >
        <h2 className='text-3xl font-bold mb-4 text-primary'>Benefits</h2>
        <ul className='font-serif pl-5'>
          <li className='mb-2'>- Increased Sales: Save time and money by finding the best deals.</li>
          <li className='mb-2'>- Lower Returns: Reduce the risk of returning items.</li>
          <li className='mb-2'>- Faster Shipping: Speed up your purchase process by using our shipping options.</li>
          <li className='mb-2'>- Customizable Products: Customize your products to fit your needs.</li>
        </ul>
        </div> */}
     

    
     
    </div>
  );
};

export default Services;