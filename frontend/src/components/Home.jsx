import React from 'react'
import { Carousel } from 'flowbite-react';
import banner3 from "../assets/banner3.jpg"
import banner2 from "../assets/banner2.jpg"
// import banner1 from "../assets/banner1.jpg"


const Home = () => {
  return (
    <div className='bg-neutral-100'>
      {/* slide 1 */}
        <div className='px-4 lg:px-14 max-w-screen-2xl mx-auto min-h-screen h-screen'>
        <Carousel className="w-full mx-auto">
        <div className="my-28 md:my-8 py-12 flex flex-col md:flex-row-reverse items-center justify-between gap-12">
          <div>
            <img className="transition-all duration-300 hover:-translate-y-4 " src={banner3} alt=""/>
          </div>
            {/* hero text */}
             <div className='md:w-1/2'>
                <h1 className='text-5xl font-semibold mb-4 text-primary'> Shop Smarter with <span className="text-blue leading-snug">the Power of AI</span></h1>
                <p className='text-primary text-base mb-8 font-serif'>We empower you to make the right choices at the right time when you shop online</p>
                <button className='btn-primary'>Discover Now</button>

             </div>
        </div>
{/* slide 2 */}
        <div className="my-28 md:my-8 py-12 flex flex-col md:flex-row-reverse items-center justify-between gap-12">
          <div>
            <img className="transition-all duration-200 hover:-translate-y-4" src={banner2} alt=""/>
          </div>
            {/* hero text */}
             <div className='md:w-1/2'>
                <h1 className='text-5xl font-semibold mb-4 text-primary'> Helps you plan your  <span className="text-blue leading-snug">next purchases</span></h1>
                <p className='text-primary text-base mb-8 font-serif'>You can keep an eye on all your saved items in one place.</p>
                <button className='btn-primary'>Discover Now</button>

             </div>
        </div>
    {/* slide 3 */}
      
    
    
      </Carousel>

        </div>

    </div>
  )
}

export default Home