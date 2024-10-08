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

// Subscribe to the channel 'holberton school channel'
client.subscribe('holberton school channel');

// When a message is received on the channel
client.on('message', (channel, message) => {
  console.log(`Received message: ${message}`);

  // If the message is 'KILL_SERVER', unsubscribe and quit
  if (message === 'KILL_SERVER') {
    client.unsubscribe('holberton school channel');
    client.quit();
  }
});
