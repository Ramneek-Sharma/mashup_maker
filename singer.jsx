import React, { useState } from 'react';

export function Singer() {
  const [formData, setFormData] = useState({
    singerName: '',
    email: '',
    numberOfAudios: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://localhost:3000/process-audio', { // Update the endpoint to match your backend
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        alert('Data sent successfully!');
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error sending data');
    }
  };

  return (
    <div className="flex items-center justify-center h-screen">
      <div className="flex flex-col items-center gap-4">
        <label className="input input-bordered flex items-center gap-2">
          <input
            type="text"
            name="singerName" // Update field name to match backend
            className="grow"
            placeholder="Singer Name"
            value={formData.singerName}
            onChange={handleChange}
            required
          />
        </label>
        <label className="input input-bordered flex items-center gap-2">
          <input
            type="email"
            name="email"
            className="grow"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </label>
        <label className="input input-bordered flex items-center gap-2">
          <input
            type="number"
            name="numberOfAudios" // Update field name to match backend
            className="grow"
            placeholder="Number of Audios"
            value={formData.numberOfAudios}
            onChange={handleChange}
            required
          />
        </label>
        <button
          className="btn relative top-2 bg-blue-500 hover:bg-blue-700 text-white font-bold p-2"
          type="button"
          onClick={handleSubmit}
        >
          Send
        </button>
      </div>
    </div>
  );
}
