import kue from 'kue';

const queue = kue.createQueue();

const jobData = {
  phoneNumber: '1234567890',
  message: 'Hello, this is a job for sending SMS.'
};

// Create a new job with the 'send_sms' type and attach the jobData
const job = queue.create('send_sms', jobData)
  .save((err) => {
    if (err) {
      console.log(`Failed to create job: ${err}`);
    } else {
      console.log(`Notification job created: ${job.id}`);
    }
  });
