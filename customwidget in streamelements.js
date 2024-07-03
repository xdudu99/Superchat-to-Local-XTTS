window.addEventListener('onEventReceived', function(obj) {
  try {
    if (!obj.detail.event) {
      return;
    }

    const listener = obj.detail.listener.split("-")[0];
    const event = obj.detail.event;

    if (listener === 'superchat') {
      const senderName = event.displayName; // Access the sender's display name
      const superchatAmount = event.amount; // Access the superchat amount
      const superchatMessage = event.message; // Access the superchat message

      // Construct the complete superchat message
      const formattedMessage = `${senderName} mandou: "${superchatMessage}"`;

      // Send superchat data to Flask server
      sendSuperchatToServer(senderName, formattedMessage);
    } else {
      console.warn('Non-superchat event received:', event);
    }
  } catch (error) {
    console.error('Error processing event:', error);
  }
});

// Function to send superchat data to Flask server
function sendSuperchatToServer(senderName, superchatMessage) {
  const data = {
    senderName: senderName,
    superchatMessage: superchatMessage
  };

  fetch('http://examplelocalhost:5000/save-superchat', { // Replace with your Flask Server
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log('Server response:', data);
    console.log('Superchat successfully saved:', data.message);
  })
  .catch(error => {
    console.error('Error saving superchat:', error);
  });
}
