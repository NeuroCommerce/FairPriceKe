import React, { useEffect, useState } from 'react';
import woman1 from '../assets/woman1.jpg';
import man2 from '../assets/man2.jpg';
import woman5 from '../assets/woman5.jpg';
import man4 from '../assets/man4.jpg';


const About = () => {
  const [inView, setInView] = useState({
    about: false,
    mission: false,
    team: false,
  });

  // Function to handle scroll and trigger animation when section is in view
  const handleScroll = () => {
    const aboutSection = document.querySelector('#about-section');
    const missionSection = document.querySelector('#mission-section');
    const teamSection = document.querySelector('#team-section');

    const aboutPos = aboutSection.getBoundingClientRect().top;
    const missionPos = missionSection.getBoundingClientRect().top;
    const teamPos = teamSection.getBoundingClientRect().top;

    const windowHeight = window.innerHeight;

    if (aboutPos < windowHeight - 100) {
      setInView(prev => ({ ...prev, about: true }));
    }
    if (missionPos < windowHeight - 100) {
      setInView(prev => ({ ...prev, mission: true }));
    }
    if (teamPos < windowHeight - 100) {
      setInView(prev => ({ ...prev, team: true }));
    }
  };

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  return (
    <div className='md:px-14 px-4 py-16 max-w-screen-2xl mx-auto bg-neutral-300 font-serif  hover duration-800 hover:-translate-x-8'>
      {/* About Us Section */}
      <div id="about-section" className={`text-center my-8 transition-all duration-700 ${inView.about ? 'opacity-100 translate-x-0' : 'opacity-0 translate-y-10'}`}>
        <h1 className='text-4xl font-semibold mb-4 text-primary'>About Us</h1>
        <p className='text-primary text-base mb-8'>
          We are a dedicated team of professionals committed to providing exceptional services and solutions. Our goal is to leverage technology to create innovative products that enhance the lives of our customers.
        </p>
      </div>

      {/* Our Mission Section */}
      <div id="mission-section" className={`text-center my-16 transition-all duration-700 ${inView.mission ? 'opacity-100 translate-x-0' : 'opacity-0 translate-y-10'}`}>
        <h2 className='text-3xl font-semibold mb-4 text-primary'>Our Mission</h2>
        <p className='text-base mb-8'>
          Our mission is to deliver high-quality, reliable, and user-friendly solutions that meet the evolving needs of our customers. We strive to be at the forefront of technological advancements and continuously improve our offerings.
        </p>
      </div>

      {/* Our Team Section */}
      <div id="team-section" className={` text-center my-16 transition-all duration-700 ${inView.team ? 'opacity-100 translate-x-0' : 'opacity-0 translate-y-10'}`}>
        <h2 className='text-3xl font-semibold mb-4 text-primary'>Our Team</h2>
        <div className='space-y-8'>
          <div className='p-4 border rounded'>
          <img src={man2} alt='Collins' className='' />
            <h3 className='text-xl font-semibold'>Collins Wamjau</h3>
            <p>CEO & Founder</p>
            <p>Collins is a Fairprice leader with over 3 years of experience in the tech industry.</p>
          </div>

          <div className='p-4 border rounded'>
          <img src={woman1} alt='Christine' className='' />
            <h3 className='text-xl font-semibold'>Christine Wakuthii</h3>
            <p>Frontend Developer</p>
            <p>Christine is an expert in software development and leads our tech team with passion and dedication.</p>
          </div>

          <div className='p-4 border rounded'>
          <img src={man4} alt='Josphat' className='' />
            <h3 className='text-xl font-semibold'>Josphat</h3>
            <p>Head of Marketing</p>
            <p>Josphat is a marketing guru who ensures our products reach the right audience.</p>
          </div>

          <div className='p-4 border rounded'>
          <img src={woman5} alt='Josphat' className='' />
            <h3 className='text-xl font-semibold'>Beth Mithamo</h3>
            <p>Data Scientist</p>
            <p>Beth is our Data Scientist pro who ensures we collect the correct data.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
