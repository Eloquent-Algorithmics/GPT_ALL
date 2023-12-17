

# I want it to work like this:

## Step one: 
    Take the users input and make a first request to get an idea of what the assistant is going to need know to fulfill the users request, check what tools are available it might need to use and or respond in the terminal with a message to the user asking for more information and have it amend the users original input to include the new information and resend the first request with the full new amended context.

## Step two:
    The first response should be a plan that first verifies it understand the users request, decides which tools to use and in which order, then creates the second request to execute the tool calls in the correct order and with the correct context.

## Step three:
    The second response is the result of the tool calls, the assistant takes all information sent and returned from the tool calls and creates a third request with the users input, the outputs from the tool calls, and instructions to use all the available inputs and responses to execute the plan. 

## Step Four
    The final response is a summarization of the responses from the tool calls and commands sent along with the final outcome and or text from the assistant answer the user request and or confirming the completion of the plan.