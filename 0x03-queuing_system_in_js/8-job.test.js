import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
  let queue;

  before(() => {
    // Initialize the queue and enter test mode
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  afterEach(() => {
    // Clear the queue after each test case
    queue.testMode.clear();
  });

  after(() => {
    // Exit the test mode after all tests
    queue.testMode.exit();
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw(
      'Jobs is not an array'
    );
  });

  it('should create jobs in the queue with valid data', () => {
    const jobs = [
      {
        phoneNumber: '1234567890',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '0987654321',
        message: 'This is the code 4321 to verify your account'
      }
    ];

    createPushNotificationsJobs(jobs, queue);

    // Validate the jobs in the queue
    expect(queue.testMode.jobs.length).to.equal(2);

    // Validate the first job data
    const job1 = queue.testMode.jobs[0];
    expect(job1.type).to.equal('push_notification_code_3');
    expect(job1.data).to.eql(jobs[0]);

    // Validate the second job data
    const job2 = queue.testMode.jobs[1];
    expect(job2.type).to.equal('push_notification_code_3');
    expect(job2.data).to.eql(jobs[1]);
  });

  it('should log job creation and progress correctly', (done) => {
    const jobs = [
      {
        phoneNumber: '4151234567',
        message: 'Test message'
      }
    ];

    createPushNotificationsJobs(jobs, queue);

    // Access the created job
    const job = queue.testMode.jobs[0];

    job.on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
      done();
    });

    job.emit('complete');
  });
});
