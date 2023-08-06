# Kitchen Sink Logger for Python
## Overview
In any running application, you literally have a split-second window where anything you want to know about that application at that moment is available. This could be anything process ID, transaction ID, user ID, etc. and/or ten other important pieces of information. If that information is not logged somewhere, it's gone forever. Maybe you could go back and piece it together from other contextual information, but you *that had that data fully in your grasp*, and if you didn't log it, you can't get it back.

The challenge with typical logging is that it's **so damn verbose** and intrusive in the code base.  For example, if I want to log a user login process, I would normally log it like this:

    logger.info('User {} logged in at {}'.format(user, datetime.now())

Let's add additional data for context:

    logger.info('User {} logged in at {}, dept_id={}, user_role={}'.format(user, datetime.now(), dept_id, user_role)

And it just gets worse from there. **DEVELOPERS HATE LOGGING BECAUSE IT'S A PAIN IN THE ASS AND THAT IS WHY I WROTE THE KITCHEN SINK LOGGER.** And don't get me started on logging metrics. Actually, you can get me started, because Kitchen Sink Logger handles metrics as well.

## Basic Concepts
### Basic Concept #1: Log Storage
Kitchen Sink Logger is super-duper simple. And it relies on the power of ElasticSearch (and it could be easily ported to any other logging destination, such as Splunk, Graylog, etc.). ElasticSearch is a no-brainer for time-stamped data in key-value pairs. In Kitchen Sink Logger, we want to log as much data as we possible can in key-value pairs, and then worry later about how we're going to search for it. That's the beauty of using ElasticSearch.

### Basic Concept #2: The Backpack
In most code logging, developers log *messages*. Unfortunately, the messages are limited to a simple sentence--honestly, because it's excruciatingly painful to piggyback additional context. So there's usually very little context and troubleshooting typically requires a developer to go back through the log messages to piece together information. 

The backpack in Kitchen Sink Logger is a concept that allows developers to add/remove key-value pairs to the backpack and those key-value pairs are automatically logged with *every single message.* This means that developers can log simple messages, but the final log entries in ElasticSearch are *packed with information.*

For example, if I want to log a user session, I can create a new logger and load the backpack with all kinds of user information one time. And then every log entry after that will contain the user information.

In this example, we're going to load the backpack with the user's ID, department and IP address. When the user logs in and then logs out, all of that information will be available in ElasticSeach for each log entry. When the user logs out, we remove those items from the backpack so when `Program done` is logged to ElasticSearch, that entry will have no backpack data. In between the `login` and `logout`, every single log message will have the user information. We add and remove any additional information at any time, such as server name, cluster name, etc.

     logger = KitchenSinkLogger()
     logger.with_item('user_id', 'tsmith')
           .with_item('dept_id', '12345')
           .with_item('ip_addr', '10.20.100.20')
     logger.info('User logged in')
     logger.info('User logged out')
     logger.without_item('user_id')
           .without_item('dept_id')
           .without_item('ip_addr')
     logger.info('Program done')

### Basic Concept #3: Sharing the Backpack
One of more common issues in dealing with serverless technology is logging across sessions. Suppose I have a data flow that runs across several lambas . . . how do I view a contiguous log across all of those sessions? Kitchen Sink Logger solves this problem by allowing you to save your backpack with a unique ID via a `StateMananger` to DynamoDB, and then re-load that backpack from any other session. This means that a Lambda can kick off a process, load the backpack with data and then save that backpack. The next Lambda can load all the data in the backpack and continue logging. As long as the backpack has a unique correlation ID, you will be able to see a perfect timeline of data flow in ElasticSearch, including all of the relevant contextual information.

####Lambda #1
	 logger = KitchenSinkLogger()
     logger.with_item('user_id', 'tsmith')
     logger.info('Doing something')
     sm = StateManager(TableName='BackpackState')
     sm.upsert(logger.backpack)

####Lambda #2
	 logger = KitchenSinkLogger()
     sm = StateManager(TableName='BackpackState')
     logger.backpack = sm.get(backpack_id)
	 logger.('Do something else')

### Basic Concept #4: Timers
One of the most commonly overlooked metrics is performance--how long are things taking. The challenge her again is that we want to see the performance across the entire application and that can be difficult in the serverless world. 

Kitchen Sink Logger solves this by allowing you to add simple named timers to the backpack. Not only are the timers added to the backpack, but every log message will have the current running time of all the timers.

This means that you can track not only the time of the overall processing of a multi-Lambda application, but you can also track the time of the individual Lambdas.

In this example, we're creating three timers: One for overall time, one for the first lambda, and one for the second lambda.

####Lambda #1
	 logger = KitchenSinkLogger()
     logger.with_timer('OverallTime')
     logger.with_timer('LambdaOneTimer')
     logger.info('Doing something')
     logger.without_timer('LambdaOneTimer')
     sm = StateManager(TableName='BackpackState')
     sm.upsert(logger.backpack)

####Lambda #2
	 logger = KitchenSinkLogger()
     sm = StateManager(TableName='BackpackState')
     logger.backpack = sm.get(backpack_id)
     logger.with_timer('LambdaTwoTimer')
	 logger.('Do something else')