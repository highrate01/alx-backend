function createPushNotificationsJobs (jobs, queue) {
  // Check if jobs is an array, if not throw an error
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }
  // Loop through each job in jobs array
  jobs.forEach((jobData) => {
    // Create a new job in the queue 'push_notification_code_3'
    const job = queue.create('push_notification_code_3', jobData);
    // On job creation, log the job ID
    job.save((err) => {
      if (!err) {
        console.log(`Notification job created: ${job.id}`);
      } else {
        console.error(`Error creating job: ${err}`);
      }
    });
    // On job completion, log the job completion
    job.on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    });
    // On job failure, log the job failure with error message
    job.on('failed', (err) => {
      console.log(`Notification job ${job.id} failed: ${err}`);
    });
    // On job progress, log the percentage of progress
    job.on('progress', (progress) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });
  });
}

export default createPushNotificationsJobs;
