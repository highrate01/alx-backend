import redis from 'redis';

const client = redis.createClient();

// On connect, log the connection message
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// On error, log the error message
client.on('error', (error) => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

// Function to publish a message to the 'holberton school channel' after a delay
function publishMessage(message, time) {
  setTimeout(() => {
    console.log(`About to send ${message}`);
    client.publish('holberton school channel', message);
  }, time);
}

// Publish messages at different intervals
publishMessage('Holberton Student #1 starts course', 100);
publishMessage('Holberton Student #2 starts course', 200);
publishMessage('KILL_SERVER', 300);
publishMessage('Holberton Student #3 starts course', 400);
