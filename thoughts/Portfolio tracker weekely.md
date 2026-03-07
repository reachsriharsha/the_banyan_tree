I want to create a portfolio tracker weekly.

Following our high-level functionalities or requirements

1. need to create a long chain agent.

2. A portfolio CSV will be provided as input, which is from broker zerodha.

3. Go through each row and find the script or the stock which is available.

4. Open browser with Trading view chart for the script/stock I will input my credentials.

5. Then credentails  will be put only once.

6. Then the agent should open a chart for that particular script and take a screenshot and save.

7. Be repeated for all the stocks in the CSV.

8. Then the agent will next move to one more task where this screenshot will be analyzed against a particular algorithm and that algorithm will be fed into the prompt.

9. As per the algorithm the image will be analysed and it should give ouput one of "HOLD, "ADD", "BUY" or EXIT. Along with reasoning from the algorithm used above

10.  After this agent will store the result along with the reason in sqlite database. This will be later used to create graphs and reports.

11. Finally a neat report in the form of markdown file will be generated with all the stocks and their respective recommendations and reasoning.

12. This process will be scheduled to run weekly, and the agent will automatically fetch the latest portfolio data from the CSV, analyze it, and generate the report without any manual intervention.

13. The agent should also have error handling mechanisms in place to manage any issues that may arise during the execution, such as network errors, issues with the CSV file, or problems with the TradingView website.

14. Additionally, the agent should be designed to be scalable, allowing for the addition of new functionalities or the ability to handle larger portfolios in the future.