import kue from 'kue';

// Blacklisted phone numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

// Function to send notification
function sendNotification(phoneNumber, message, job, done) {
  // Track job progress to 0%
  job.progress(0, 100);

  // Check if phone number is blacklisted
  if (blacklistedNumbers.includes(phoneNumber)) {
    // Fail the job if phone number is blacklisted
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  } else {
    // Track progress to 50%
    job.progress(50, 100);
    
    // Log the notification message
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
    
    // Simulate job completion
    setTimeout(() => {
      job.progress(100, 100);
      done();
    }, 1000);
  }
}

// Create Kue queue
const queue = kue.createQueue();

// Process jobs from the 'push_notification_code_2' queue, max 2 jobs at a time
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});

console.log('Job processor is running...');
