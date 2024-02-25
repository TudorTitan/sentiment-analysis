1. **Connect to MongoDB database**
  Use the password I sent you, and the email "teodor.ciurca@gmail.com" to log into MongoDB and "add current IP address". Then click "connect" to connect to database. I think you only need to do this once, but if you ever fail to connect to the database, repeat this step.
2. **Add API keys**
  Replace YOURPASSWORD in line 6 of pymongo_get_database.py with the password I sent you.
  Set the OpenAI API key I sent you as a permanent environment variable: Go to https://platform.openai.com/docs/quickstart?context=python, Under set up your API key, under set up your API key for all projects (recommended), under Windows, follow step 3 (permanent setup)
3. **How to add articles**
  Add article to a file called "article.txt", same folder as project. Then call add_article(te) from pull_article.py
