import React from 'react';

const Contact = () => {
  return (
    <div className='md:px-14 px-4 py-16 max-w-screen-2xl mx-auto bg-neutral-100 border'>
      <div className='text-center my-8'>
        <h1 className='text-4xl font-semibold mb-4 text-primary'>Contact Us</h1>
        <p className='text-primary text-base mb-8'>
          If you have any questions or would like to get in touch, please fill out the form below and we will get back to you as soon as possible.
        </p>
      </div>

      <form className='space-y-4'>
        <div>
          <label className='block mb-2 text-sm font-medium text-gray-700'>Name</label>
          <input type='text' className='w-full p-2 border rounded' placeholder='Your Name' />
        </div>
        <div>
          <label className='block mb-2 text-sm font-medium text-gray-700'>Email</label>
          <input type='email' className='w-full p-2 border rounded' placeholder='Your Email' />
        </div>
        <div>
          <label className='block mb-2 text-sm font-medium text-gray-700'>Subject</label>
          <input type='text' className='w-full p-2 border rounded' placeholder='Subject' />
        </div>
        <div>
          <label className='block mb-2 text-sm font-medium text-gray-700'>Message</label>
          <textarea className='w-full p-2 border rounded' rows='4' placeholder='Your Message'></textarea>
        </div>
        <button type='submit' className='px-4 py-2 bg-primary text-white rounded'>Submit</button>
      </form>
    </div>
  );
};

export default Contact;